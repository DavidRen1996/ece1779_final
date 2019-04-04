class PrivateUserInfo:
    def __init__(self, username, password, interested_photos_map, pending_requests_map,
                 received_inquiries_map):
        self.username = username
        self.password = password
        self.interested_photos_map = interested_photos_map
        self.pending_requests_map = pending_requests_map
        self.received_inquiries_map = received_inquiries_map
