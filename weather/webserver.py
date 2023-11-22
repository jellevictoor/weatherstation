import json
import socket

import uasyncio


class WebServer:
    def __init__(self, config):
        self._output_file = config['output_file']

    def listen(self) -> uasyncio.Server:
        print("Starting webserver...")
        return uasyncio.start_server(self._serve, '0.0.0.0', 80)

    def _get_payload(self, request):
        request = str(request)
        status = request.find('/status')
        last = request.find('/last')
        payload = None
        if status >= 0:
            payload = json.dumps({'status': 'ok'})
        elif last >= 0:
            with open(self._output_file, 'r') as infile:
                json_data = json.load(infile)
                payload = json.dumps(json_data)
        return payload

    async def _serve(self, reader: uasyncio.StreamReader, writer: uasyncio.StreamWriter):
        try:
            print("HTTP-Client Connected...")
            request = str(await reader.read(1024))
            print(request)
            payload = self._get_payload(request)
            await writer.awrite('HTTP/1.1 200 OK\r\n')
            await writer.awrite('Connection: close\r\n')
            await writer.awrite('Content-Type: application/json\r\n\r\n')
            await writer.awrite(payload)

            await reader.wait_closed()
            await writer.drain()
            await writer.wait_closed()

        except Exception as e:
            print(e)
