from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import LocationMediaMessageProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import VCardMediaMessageProtocolEntity

import os, subprocess

message = 'yo'
authorisednumber = '6590675647'
macs = {}
macs[0,0] = "D8:96:95:12:01:02"; macs[0,1] = "Max iPhone"
macs[1,0] = "F0:Cb:A1:60:56:D3"; macs[1,1] = "Steven"
macs[2,0] = "80:EA:96:3B:2B:01"; macs[2,1] = "Gerry"


class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if not messageProtocolEntity.isGroupMessage():
            if messageProtocolEntity.getType() == 'text':
                self.onTextMessage(messageProtocolEntity)
            elif messageProtocolEntity.getType() == 'media':
                self.onMediaMessage(messageProtocolEntity)
    
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)

    def onTextMessage(self,messageProtocolEntity):
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
        recipient = messageProtocolEntity.getFrom(False)
        sendto = messageProtocolEntity.getFrom()
        messagereceived = messageProtocolEntity.getBody().lower()

        #send receipt otherwise we keep receiving the same message over and over
        self.toLower(receipt)


        #Generate responses based on commands received
        if messagereceived == message.lower() :
            self.ReplyWith("Hi, i'm a RaspberryPi", sendto)

        elif messagereceived == "reboot":
            if recipient == authorisednumber:
                self.ReplyWith("rebooting..", sendto)
                os.system("sudo reboot")
            else:
                self.ReplyWith("NOT AUTHORISED", sendto)

        elif messagereceived == "nmap":
            result = subprocess.check_output("sudo nmap -sn 192.168.2.1-100", shell=True)
            #self.ReplyWith(result, sendto)

            for row in macs:
                print(macs[row,0])
                print("\n")

                





        else :
            reponse = "invalid command"
            self.ReplyWith("Invalid command laaa", sendto)

        # outgoingMessageProtocolEntity = TextMessageProtocolEntity(
        #     response,
        #     to = messageProtocolEntity.getFrom())

        # self.toLower(outgoingMessageProtocolEntity)       





    def ReplyWith(self, response, recipient):

        outgoingMessageProtocolEntity = TextMessageProtocolEntity(
             response,
             to = recipient)

        self.toLower(outgoingMessageProtocolEntity)

        print("Replying %s to %s" % (response, recipient))        

    def onMediaMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getMediaType() == "image":
            
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())

            outImage = ImageDownloadableMediaMessageProtocolEntity(
                messageProtocolEntity.getMimeType(), messageProtocolEntity.fileHash, messageProtocolEntity.url, messageProtocolEntity.ip,
                messageProtocolEntity.size, messageProtocolEntity.fileName, messageProtocolEntity.encoding, messageProtocolEntity.width, messageProtocolEntity.height,
                messageProtocolEntity.getCaption(),
                to = messageProtocolEntity.getFrom(), preview = messageProtocolEntity.getPreview())

            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

            #send receipt otherwise we keep receiving the same message over and over
            self.toLower(receipt)
            self.toLower(outImage)

        elif messageProtocolEntity.getMediaType() == "location":

            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())

            outLocation = LocationMediaMessageProtocolEntity(messageProtocolEntity.getLatitude(),
                messageProtocolEntity.getLongitude(), messageProtocolEntity.getLocationName(),
                messageProtocolEntity.getLocationURL(), messageProtocolEntity.encoding,
                to = messageProtocolEntity.getFrom(), preview=messageProtocolEntity.getPreview())

            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

            #send receipt otherwise we keep receiving the same message over and over
            self.toLower(outLocation)
            self.toLower(receipt)
        elif messageProtocolEntity.getMediaType() == "vcard":
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
            outVcard = VCardMediaMessageProtocolEntity(messageProtocolEntity.getName(),messageProtocolEntity.getCardData(),to = messageProtocolEntity.getFrom())
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
            #send receipt otherwise we keep receiving the same message over and over
            self.toLower(outVcard)
            self.toLower(receipt)
