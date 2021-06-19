import ssl.encryption.CertSigningRequest as req 
import ssl.encryption.SignCert as signer
import ssl.encryption.CertX509Gen as gen




while True:
    action = input("Choose what you want to do.\nAvailable actions: CREATE_CERT_REQ, SIGN_CERT, GEN_ROOT_CERT, END :\n")
    if( action == "CREATE_CERT_REQ" ):
        print("You have choosen certificate signing request")
        req.main()

    elif( action == "SIGN_CERT" ):
        print("You have choosen signing certificate request with your root cert")
        signer.main()

    elif( action == "GEN_ROOT_CERT" ):
        print("You have choosen self signed root cert creation")
        gen.main()

    elif( action == "END" ):
        break
    else: 
        print("This action doesn't exists")


