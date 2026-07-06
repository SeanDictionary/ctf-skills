param(
  [string]$RemoteHost = "172.17.122.193",
  [string]$User = "sean",
  [string]$IdentityFile = "$env:USERPROFILE\\.ssh\\id_rsa",
  [Parameter(Mandatory = $true)]
  [string]$Payload
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-SystemSshExe {
  function Test-MicrosoftSigned([string]$Path) {
    try {
      $sig = Get-AuthenticodeSignature -FilePath $Path
      if ($sig.Status -ne "Valid") { return $false }
      if (-not $sig.SignerCertificate) { return $false }
      return ($sig.SignerCertificate.Subject -like "*Microsoft*")
    } catch {
      return $false
    }
  }

  $candidates = @(
    (Join-Path $env:WINDIR "System32\\OpenSSH\\ssh.exe"),
    (Join-Path $env:WINDIR "Sysnative\\OpenSSH\\ssh.exe")
  )

  foreach ($p in ($candidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique)) {
    if (Test-MicrosoftSigned -Path $p) { return $p }
  }

  $cmd = Get-Command ssh.exe -ErrorAction SilentlyContinue
  if ($cmd -and $cmd.Source -and ($cmd.Source -like "C:\\Windows\\*") -and (Test-Path $cmd.Source)) {
    if (Test-MicrosoftSigned -Path $cmd.Source) { return $cmd.Source }
  }

  $hint = Join-Path $env:WINDIR "System32\\OpenSSH\\ssh.exe"
  throw ("System OpenSSH client not found (or not Microsoft-signed). Expected something like: {0}`n" -f $hint) +
        "Install Windows Optional Feature 'OpenSSH Client', or run an elevated PowerShell:`n" +
        "  Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0"
}

$sshExePath = Resolve-SystemSshExe
$nullHostsFile = "NUL"

$identityArgs = @()
if ($IdentityFile) {
  try {
    # In some locked-down / sandboxed sessions, reading under ~/.ssh can throw AccessDenied.
    # If we can't stat the file, just let ssh.exe use its normal key discovery.
    if (Test-Path -LiteralPath $IdentityFile) {
      $identityArgs = @("-i", $IdentityFile)
    }
  } catch {
    $identityArgs = @()
  }
}

# Build a bash payload, then base64-encode it to avoid fragile quoting rules and stdin encoding issues.
$remoteBash = @'
set -eo pipefail
source ~/.bashrc >/dev/null 2>&1 || true
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
  source "$HOME/miniforge3/etc/profile.d/conda.sh"
elif [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/anaconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/mambaforge/etc/profile.d/conda.sh" ]; then
  source "$HOME/mambaforge/etc/profile.d/conda.sh"
elif command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
fi
export TERM=xterm
conda activate sage
__PAYLOAD__
'@
$remoteBash = $remoteBash.Replace("__PAYLOAD__", $Payload)
$remoteBash = $remoteBash -replace "`r`n", "`n"

$b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($remoteBash))
$remoteCmd = "printf '%s' '$b64' | base64 -d | bash"

$sshArgs = @()
$sshArgs += $identityArgs
$sshArgs += @(
  "-o", "BatchMode=yes",
  "-o", "ConnectTimeout=15",
  "-o", "LogLevel=ERROR",
  # Keep this non-interactive and robust even if ~/.ssh/{config,known_hosts} are inaccessible.
  "-o", "StrictHostKeyChecking=no",
  "-o", ("UserKnownHostsFile=" + $nullHostsFile),
  "-o", ("GlobalKnownHostsFile=" + $nullHostsFile),
  "$User@$RemoteHost",
  $remoteCmd
)

& $sshExePath @sshArgs
exit $LASTEXITCODE
