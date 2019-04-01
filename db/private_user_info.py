class PrivateUserInfo:
    def __init__(self, username, encrypted_password, interested_photos, pending_requests, received_inquiries):
        self.username = username
        self.encrypted_password = encrypted_password
        self.interested_photos = interested_photos
        self.pending_requests = pending_requests
        self.received_inquiries = received_inquiries
