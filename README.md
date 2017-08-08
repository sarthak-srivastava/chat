# chat
This project focuses on the major problem faced by django web applications,i.e, real time interaction between server and the client. The material source of this project can be found at :
http://channels.readthedocs.io/en/stable/concepts.html
https://gearheart.io/blog/creating-a-chat-with-django-channels/ .

Django-channels consist of three components:

Interface servers - which handle requests (WSGI and ASGI) and put them in a queue.

Channels - is a first-in first-out queue for messages that need to be stored in data structures such as Redis, IPC etc. The message can be delivered only to one listener, message delivery order depends only on its getting into the queue.

Workers - monitor channels and handle requests.





:)
