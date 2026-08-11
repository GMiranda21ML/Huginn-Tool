import subprocess


def run(cmd, cwd=None):
    """Executa cmd, mostrando a saída em tempo real, e devolve (returncode, saida_completa)."""
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    lines = []
    for line in process.stdout:
        print(line, end="")
        lines.append(line)
    process.wait()
    return process.returncode, "".join(lines)


def capture(cmd, cwd=None):
    """Executa cmd sem transmitir a saída, e devolve (returncode, stdout, stderr)."""
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode, result.stdout, result.stderr


def which(binary):
    result = subprocess.run(
        ["which", binary], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return result.returncode == 0
