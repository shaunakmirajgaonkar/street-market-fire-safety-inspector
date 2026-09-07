import socket, subprocess, sys

def free_port(start=8501,end=8599):
    for p in range(start,end+1):
        with socket.socket() as s:
            try:
                s.bind(('127.0.0.1',p)); return p
            except OSError:
                continue
    raise RuntimeError('No free localhost port found.')

port=free_port()
print(f'Starting FireWatch on http://localhost:{port}')
subprocess.run([sys.executable,'-m','streamlit','run','app.py','--server.address=localhost',f'--server.port={port}'],check=True)
