# Wireshark and TShark Filter Notes

## Core Display Filters

- `ip.addr == 10.10.10.10`
  Limit traffic to one host.
- `tcp.stream eq 5`
  Follow one TCP conversation.
- `udp.stream eq 3`
  Follow one UDP conversation when stream indexes exist.
- `http`
  Show all HTTP packets.
- `http.request`
  Focus on client requests.
- `dns`
  Show DNS traffic.
- `dns.flags.response == 0`
  Show only DNS queries.
- `tls.handshake.extensions_server_name`
  Extract TLS SNI hostnames.
- `icmp`
  Check beaconing, reachability tests, or data hidden in payloads.
- `tcp.flags.syn == 1 && tcp.flags.ack == 0`
  Show connection attempts.
- `tcp.analysis.retransmission`
  Surface unstable flows or noisy captures.
- `frame contains "flag{"`
  Fast literal search for common flag strings.

## Common TShark Patterns

```powershell
& 'D:\Wireshark\tshark.exe' -r '.\Traffic.pcapng' -q -z io,phs
& 'D:\Wireshark\tshark.exe' -r '.\Traffic.pcapng' -q -z endpoints,ip -z conv,tcp -z conv,udp
& 'D:\Wireshark\tshark.exe' -r '.\Traffic.pcapng' -Y 'http.request' -T fields -e frame.number -e ip.src -e http.host -e http.request.uri
& 'D:\Wireshark\tshark.exe' -r '.\Traffic.pcapng' -Y 'dns.flags.response == 0' -T fields -e frame.number -e dns.qry.name
& 'D:\Wireshark\tshark.exe' -r '.\Traffic.pcapng' -q -z follow,tcp,ascii,0
```

## Evidence Checklist

- Record the packet number that proves the conclusion.
- Save the exact display filter used to isolate the finding.
- Prefer at least two agreeing signals when the capture is noisy.
- If HTTP or SMB suggests transferred files, export or reconstruct only after you know which stream matters.
