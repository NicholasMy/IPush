class IpSource:
    def get_ipv4(self) -> str:
        raise NotImplementedError

    def get_ipv6(self) -> str:
        raise NotImplementedError

    def get_ipv(self, v: int):
        if v == 4:
            return self.get_ipv4()
        elif v == 6:
            return self.get_ipv6()
        else:
            raise ValueError(f"Invalid IP version {v}.")
