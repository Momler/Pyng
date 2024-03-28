# Pyng
A complete implementation of the well known `ping` program under windows, using `python 3.10.0` with no dependencies.
The outputs and the flags correspond 1:1 to the windows implementation.

## Fixes

There are things that the Windows ping implementation does wrong, but are fixed in this project.

1. The [Windows documentation](https://learn.microsoft.com/de-de/windows-server/administration/windows-commands/ping) claims that if the `-a` flag is specified, the corresponding hostname of the IP address will be resolved. However, this happens by default and cannot be deactivated. Accordingly, the `-a` has no use under the Windows implementation and is permanently active.

## How to use
Simply execute `Pyng.py` with the known arguments from the standard `ping`:

`python .\src\Pyng.py 127.0.0.1`

which results with the following output:
```

Ping wird ausgeführt für 127.0.0.1 mit 40 Bytes Daten:
Antwort von 127.0.0.1: Zeit=0ms
Antwort von 127.0.0.1: Zeit=0ms
Antwort von 127.0.0.1: Zeit=0ms
Antwort von 127.0.0.1: Zeit=0ms

Ping-Statistik für 127.0.0.1:
    Pakete: Gesendet = 4, Empfangen = 4, Verloren = 0
    (0% Verlust),
Ca. Zeitangaben in Millisek.:
    Minimum = 0ms, Maximum = 0ms, Mittelwert = 0.0ms 

```