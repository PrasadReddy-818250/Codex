from __future__ import annotations

import socket
import subprocess
from dataclasses import dataclass

from assistant.config import AppConfig


@dataclass(frozen=True)
class RuntimeStatus:
    running: bool
    host: str
    port: int
    pid: int | None = None
    message: str = ""


class RuntimeManager:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def status(self) -> RuntimeStatus:
        pid = self._pid_on_port(self.config.llama_port)
        return RuntimeStatus(
            running=pid is not None,
            host=self.config.llama_host,
            port=self.config.llama_port,
            pid=pid,
            message="running" if pid is not None else "stopped",
        )

    def start(self) -> RuntimeStatus:
        current = self.status()
        if current.running:
            return RuntimeStatus(
                running=True,
                host=current.host,
                port=current.port,
                pid=current.pid,
                message="llama-server is already running",
            )
        if not self.config.llama_server_path.exists():
            return RuntimeStatus(
                running=False,
                host=self.config.llama_host,
                port=self.config.llama_port,
                message=f"llama-server.exe not found: {self.config.llama_server_path}",
            )
        if not self.config.llama_model_path.exists():
            return RuntimeStatus(
                running=False,
                host=self.config.llama_host,
                port=self.config.llama_port,
                message=f"model not found: {self.config.llama_model_path}",
            )

        args = [
            str(self.config.llama_server_path),
            "-m",
            str(self.config.llama_model_path),
            "--host",
            self.config.llama_host,
            "--port",
            str(self.config.llama_port),
            "-c",
            str(self.config.llama_context_size),
            "-t",
            str(self.config.llama_threads),
        ]
        subprocess.Popen(
            args,
            cwd=str(self.config.llama_server_path.parent),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return RuntimeStatus(
            running=True,
            host=self.config.llama_host,
            port=self.config.llama_port,
            pid=None,
            message="llama-server start requested",
        )

    def stop(self) -> RuntimeStatus:
        pid = self._pid_on_port(self.config.llama_port)
        if pid is None:
            return RuntimeStatus(
                running=False,
                host=self.config.llama_host,
                port=self.config.llama_port,
                message="llama-server is already stopped",
            )
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/F"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return RuntimeStatus(
            running=False,
            host=self.config.llama_host,
            port=self.config.llama_port,
            pid=pid,
            message=f"llama-server stop requested for PID {pid}",
        )

    def _pid_on_port(self, port: int) -> int | None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.25)
            if probe.connect_ex((self.config.llama_host, port)) != 0:
                return None

        result = subprocess.run(
            ["netstat", "-ano"],
            check=False,
            capture_output=True,
            text=True,
        )
        needle = f"{self.config.llama_host}:{port}"
        for line in result.stdout.splitlines():
            if needle in line and "LISTENING" in line:
                parts = line.split()
                if parts and parts[-1].isdigit():
                    return int(parts[-1])
        return None
