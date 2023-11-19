import json
import socket



class WebServer:
    def __init__(self, config):
        self._output_file = config['output_file']

        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        self._socket = socket.socket()
        self._socket.bind(addr)
        self._socket.listen(1)

        print('listening on', addr)


    async def _listen(self):
        print('listening')
        while True:
            try:
                cl, addr = self._socket.accept()
                request = cl.recv(1024)
                request = str(request)
                status = request.find('/status')
                last = request.find('/last')

                payload = None
                if status >= 0:
                    payload = json.dumps({'status': 'ok'})
                elif last >= 0:
                    with open(self._output_file, 'r') as infile:
                        payload = json.load(infile.read())

                if payload is not None:
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
                    cl.send(payload)
                    cl.close()
                    continue
                else:
                    cl.send('HTTP/1.0 404 Not Found\r\nContent-type: text/html\r\n\r\n')

            except OSError as e:
                cl.close()
                print('connection closed')
