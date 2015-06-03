from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import LocationMediaMessageProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import VCardMediaMessageProtocolEntity

import os, subprocess

import ltadatamall

#for converting time stampe from LTADATAMALL
from datetime import datetime, timedelta

message = 'yo'
authorisednumber = '6590675647'

macaddresses = [ [ "D8:96:95:12:01:02", "F0:Cb:A1:60:56:D3", "7C:FA:DF:BD:0A:17", "80:ea:96:3b:2b:01", "28:E1:4C:A9:64:3E", "F0:25:B7:18:60:1F", "e4:ce:8f:4b:72:72"] , [ "Max iPhone", "Steven", "Gerry", "Peilynn", "Mylene", "Jia Jia", "Gerry's Macbook" ] ]


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
            self.ReplyWith(result, sendto)

        elif messagereceived == "whoishome":
            result = subprocess.check_output("sudo nmap -sn 192.168.2.1-100", shell=True)
            #self.ReplyWith(result, sendto)

            for mac in xrange(len(macaddresses[0])):
                if macaddresses[0][mac].upper() in result:
                    self.ReplyWith(macaddresses[1][mac] + " is home", sendto)

            self.ReplyWith("-- End of List --", sendto)
                
        elif messagereceived == "traffic":
            results = ltadatamall.traffic()
            for x in results["d"]:
                #print(jsonObj["d"][str(x)]["Message"])
                self.ReplyWith(x["Message"],sendto)

        elif messagereceived == "shutdownnas":
            if recipient == authorisednumber:

                self.shutdownnas()
                self.WirelessSwitchOff()
                self.ReplyWith("Shutting down MAX-NAS",sendto)

            else:
                self.ReplyWith("NOT AUTHORISED",sendto)


        elif messagereceived == "powerswitchon":
            if recipient == authorisednumber:

                self.WirelessSwitchOn()

            else:
                self.ReplyWith("NOT AUTHORISED",sendto)

        elif messagereceived == "powerswitchoff":
            if recipient == authorisednumber:

                self.WirelessSwitchOff()

            else:
                self.ReplyWith("NOT AUTHORISED",sendto)                

        elif messagereceived == "bustotown":

            self.QueryBus("972","44691",sendto)
            self.QueryBus("922","44691",sendto)

        elif messagereceived == "bustobpp":
            self.QueryBus("972","44699",sendto)
            self.QueryBus("922","44699",sendto)


        elif messagereceived == "busfrombpp":
            self.QueryBus("972","44614",sendto)
            self.QueryBus("922","44614",sendto)

        elif messagereceived == "busfromcck":
            self.QueryBus("190","44539",sendto)
            self.QueryBus("975","44539",sendto)


        elif messagereceived == "busfromlakeside":
            self.QueryBus("180","28099",sendto)

        elif messagereceived == "busfromtj":
            self.QueryBus("98","21591",sendto)            
            self.QueryBus("98M","21591",sendto)            
            self.QueryBus("240","21591",sendto)            
            self.QueryBus("246","21591",sendto)            

        elif messagereceived == "busfromnex":

            self.QueryBus("109","66009",sendto)
            self.QueryBus("103","66009",sendto)
            self.QueryBus("317","66009",sendto)


        else :
            reponse = "invalid command"
            self.ReplyWith("Invalid command", sendto)

        # outgoingMessageProtocolEntity = TextMessageProtocolEntity(
        #     response,
        #     to = messageProtocolEntity.getFrom())

        # self.toLower(outgoingMessageProtocolEntity)       



    def shutdownnas():

        os.system("ssh -i /home/pi/.ssh/id_rsa root@192.168.2.50 poweroff")

    def WirelessSwitchOff(self):

        os.system("sudo /home/pi/Projects/maxapp/codesend/codesend 6642535")

    def WirelessSwitchOn(self):

        os.system("sudo /home/pi/Projects/maxapp/codesend/codesend 6642543")

    def QueryBus(self, Bus, BusStopNo, sendto):

        results = ltadatamall.bus(Bus,BusStopNo)
#asd
        for x in results["Services"]:
            NextBusTS = x["NextBus"]["EstimatedArrival"]
            NextBusTS2 = datetime.strptime(NextBusTS, "%Y-%m-%dT%H:%M:%S+00:00") + timedelta(hours=9) #convert to GMT +8
            NextBusLoad = x["NextBus"]["Load"]
            #print "922 Next Bus: " + newtimestamp
            SubBusTS = x["SubsequentBus"]["EstimatedArrival"]
            SubBusLoad = x["SubsequentBus"]["Load"]
            SubBusTS2 = datetime.strptime(SubBusTS, "%Y-%m-%dT%H:%M:%S+00:00") + timedelta(hours=9)
            self.ReplyWith(str(Bus) + " Next Bus: " + str(datetime.time(NextBusTS2)) + " (" + str(NextBusLoad) + ")" + " Subsequent: " + str(datetime.time(SubBusTS2)) + " (" + str(SubBusLoad) + ")",sendto)


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
