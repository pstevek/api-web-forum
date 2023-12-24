INSERT INTO roles (id, slug, name, created_at, updated_at, deleted_at)
VALUES
    (1, 'moderator', 'Moderator', current_timestamp, NULL, NULL),
    (2, 'regular', 'Regular', current_timestamp, NULL, NULL);

INSERT INTO users (id, role_id, username, email, first_name, last_name, password, created_at, updated_at, deleted_at)
VALUES
    (1, 1, 'admin', 'admin@gmail.com', 'Admin', 'User', '$2b$12$iwXgcPqwGTQ5qDyIglHD.OP7DfizRxAL1RdpOzYtsx6GPaiJIoluK', current_timestamp, NULL, NULL),
    (2, 2, 'pstevek', 'steve.kamanke@gmail.com', 'Steve', 'Kamanke', '$2b$12$ZM2s4fEesOawfUOjcb553u3gRnL3z/njdcddq3OeWoj4NqX7wgbeq', current_timestamp, NULL, NULL);
