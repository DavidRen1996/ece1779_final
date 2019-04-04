class PrivateUserInfo:
    def __init__(self, username, password, interested_photos_list, pending_requests_map,
                 received_inquiries_map):
        self.username = username
        self.password = password
        self.interested_photos_list = interested_photos_list
        self.pending_requests_map = pending_requests_map
        self.received_inquiries_map = received_inquiries_map
