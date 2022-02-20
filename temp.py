def threaded_client(connection):
    connection.send(str.encode('CONNECTED'))
    while True:
        data = connection.recv(socketSize)
        if not data:
        break
        (key, encryptedQuestion, hashy) = pickle.loads(data)
        f = Fernet(key)
        hashy = str(hashy)
        checkHashy = hashlib.md5(encryptedQuestion)
        checkHashy = checkHashy.hexdigest()
        encryptedQuestion = encryptedQuestion.decode("utf-8")
        if (checkHashy == hashy)
            notEncrypted = f.decrypt(encryptedQuestion.encode())
            question = notEncrypted
            print('[Server ' + str(time.time()) + '] -- Plain Text: ' + question)
            client = wolframalpha.Client(app_id)
            if not question:
                break
            res = client.query(question)
            print('[Server ' + str(time.time()) + '] -- Sending question to WolframAlpha')
            answer = next(res.results).text
            print('[Server ' + str(time.time()) + '] -- Received answer from WolframAlpha: ' + answer)
            reply = answer
            connection.sendall(str.encode(reply))
    connection.close()
    print ('DISCONNECTED')
