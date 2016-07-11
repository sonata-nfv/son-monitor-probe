import json

class server(object):
    def __init__(self, server_):
        self.id = server_["id"]
        self.status = server_["status"]
        self.updated = server_["updated"]
        self.hostId = server_["hostId"]
        self.hostName = server_["OS-EXT-SRV-ATTR:hypervisor_hostname"]
        self.addresses = server_["addresses"]
        self.imageId = server_["image"]["id"]
        self.launched = server_["OS-SRV-USG:launched_at"]
        self.flavorId = server_["flavor"]["id"]
        self.security_groups = server_["security_groups"]
        self.name = server_["name"]
        self.useId = server_["user_id"]
        self.tenantId = server_["tenant_id"]
        self.volumes = server_["os-extended-volumes:volumes_attached"]
        
    def addDgn(self,diagnostics_):
        self.diagnostics = diagnostics_