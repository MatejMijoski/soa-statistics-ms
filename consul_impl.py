from consul import Consul, Check

consul_port = 8500
service_name = "statistics"
service_port = 5007


def register_to_consul():
    consul = Consul(host="consul", port=consul_port)
    agent = consul.agent
    service = agent.service
    check = Check.http(f"http://{service_name}:{service_port}/", interval="10s", timeout="5s", deregister="1s")
    service.register(service_name, service_id=service_name, port=service_port, check=check)


def get_service(service_id):
    consul = Consul(host="consul", port=consul_port)
    agent = consul.agent
    service_list = agent.services()
    service_info = service_list[service_id]
    return service_info['Address'], service_info['Port']

register_to_consul()

