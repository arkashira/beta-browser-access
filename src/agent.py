import argparse
import json
import dataclasses
import os
import platform

@dataclasses.dataclass
class AgentConfig:
    user: str
    encryption: str

def create_agent_config(user: str, encryption: str) -> AgentConfig:
    return AgentConfig(user, encryption)

def run_agent(agent_config: AgentConfig) -> None:
    if platform.system() == 'Windows':
        if os.getlogin() != 'NT AUTHORITY\\LocalService':
            raise RuntimeError('Agent must run as Local Service account')
    elif platform.system() in ['Linux', 'Darwin']:
        if os.getuid() != 0 or os.geteuid() != 0:
            raise RuntimeError('Agent must run under a dedicated low-privilege user')
    if agent_config.encryption != 'TLS 1.3':
        raise RuntimeError('All network traffic must be encrypted via TLS 1.3')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', help='Dedicated low-privilege user')
    parser.add_argument('--encryption', help='Encryption protocol')
    args = parser.parse_args()
    agent_config = create_agent_config(args.user, args.encryption)
    run_agent(agent_config)

if __name__ == '__main__':
    main()
