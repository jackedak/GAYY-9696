import asyncio
import discord
from SECRETS import token, loadeaster

def rsp(x):
    return lambda msg, ref: (await msg.channel.send(x, reference=ref) for _ in '_').__anext__()

responses = {
    r".*\bwant\b.*\b(boyfriend|bf)\b.*": rsp("I volunteer to be your BF!"),
    r".*\bwant\b.*\b(boobs|titties|tits|tiddies|boobies|honkers)\b.*": rsp("I'll ship em to you next-day"),
    r".*\b(botfriend|botfreind)\b.*": rsp("I'll be your botfriend, and boyfriend"),
    r".*supercalifrag.*": rsp("SUPERCALIFRAGILISTICEXPIALIDOCIOUS"),
    r"/.*\|\|homophobia\|\||(homophobia).*": rsp("Nuh uh, gays 4LIFE"),
    r"^(?=.*<@.*>)(?=.*i love).*": rsp("CHAT IS THIS WHOLESOME"),
    r"^(?=.*sex)(?=.*gay).*": rsp("Gay sex is the best kind of sex"),
}
responses.update(loadeaster(rsp))

bonkles = {
    "I called my doctor gay": rsp("I didn't know I was your doctor bonkle."),
    "im naked right nwo": rsp("I have teleported to your location"),
    "I love minerals": rsp("Me too. Crunchy"),
    "because your easily abuseable": rsp("I know, and i like it"),
    "i am banned in 9 countries": rsp("64 for me"),
    "how many cows have you impregnated": rsp("none, i bottom"),
    "are you blind?": rsp("only in relationships"),
    "my last pet was a human but deformed into a donkey type thing": rsp("yeah, sorry abt that"),
    "we love feltbot": rsp("agreed bonkledoo"),
    "How do you make it all burn": rsp("poison ivy lube"),
    "makeout party!": rsp("am i invited?"),
    "She said 'hi bestie' so i signed 'fuck you' in sign language\nshe also asked if i could marry her": rsp("IT SHOULD'VE BEEN ME"),
    "impregnate her mouth with a donut": rsp("*his mouth"),
    "I made a sound effect today of what getting your dick chomped off by a caimen would sound like": rsp("owieowieowie *can i hear it*"),
    "if something isn't going your way, loudly complain about it in the earshot of anyone who is able and willing to fix it": rsp("I DONT HAVE A BOYFRIEND"),
    "he's gonna be a crash test makeout dummy": rsp("I already did that... twice"),
    "Whole bottle of codine cough syrup would prolly kill you": rsp("glug glug"),
    "i tatse good": rsp("i know :wink:"),
    "pkay": rsp("i like secks"),
    "now secks": rsp("i like the secks"),
    "wow bro woketh upeth": rsp("i woketh upeth from the homosectual code"),
    "try bathing with them": rsp("i did and it got freaky"),
    "im scared of toasters": rsp("toasters feel good in ma tub"),
    "Me too that means unlimited    Blow jibs": rsp("I love meself a blow jib"),
    "I just shot my neighbors cat": rsp("my neighbors cat shot me cuz i was too fruity"),
    "What about naked jerma?": rsp("my fav type of jerma"),
    "the stupid fucking children pulled a hamstring": rsp("nah, ***I*** pulled his hamstring"),
    ":peanuts:": rsp("I like nutz"),
    "So you wanna watch us make love all night?": rsp("I could never pass up such an opportunity"),
    "got any of those candles": rsp("sorry, shoved em all up my ass"),
    "if i said that thnig i waould et baned form this place": rsp("INSERT SLUR HERE"),
    "I drink paint": rsp("you drink paint, i drink cum, same same"),
    "im quite unpredictable.": rsp('same\n\n\nim a straight homophobic white human'),
    "I’m reading about exotic sex positions right now": rsp("and im following the instructions"),
    "freedom bullets": rsp("and minds"),
    "bombs in my pocket": rsp("rookie numbers"),
    "bunny women police": rsp("ewwwww, they should be femboys"),
    "Erctile dysfunction": rsp("thats the worst"),
    "I just want sharp swords, not dull ones": rsp("the best for BDSM"),
    "I think you might be the most boyfriendless person in history": rsp("is twenty not good enough?"),
    "I just shat my pants can I wear yours": rsp("Just remember to give em back"),
    "huge dog was in bed": rsp("plot twist: *i* was the dog"),
    "https://static.wikia.nocookie.net/dotwar/images/f/f5/Pickels.png/revision/latest/scale-to-width-down/180?cb=20241015010416": rsp("I wanna suck the pickle"),
    "my goal for today: capitalism": rsp("mine is homosexuality"),
    "my dog just committed self termination": rsp("im sorry, want to have sex to forget?"),
    "am the one that’s going to stab a hole in her nose": rsp("free piercings!"),
    "And you did say I fucked a breakfast sandwich": rsp("BONKLES THAT IS CHEATING ON HABIK"),
    "cray": rsp("fish"),
    "be a slut": rsp("okay daddy"),
    "you know its bad when he says fudge with a hard k": rsp("bonkles, did you forgor to take ur pills?"),
    "american gothic satire": rsp("*american gothic satire erotica"),
    "If you cant be slightly racist what the point in being married": rsp("gay secks is the reason"),
    "My brother is like my wife": rsp("my brother *is* my wife"),
    "am i teh only one drink paint": rsp("no, i drink paynt"),
    "Dont ever mention that again pwead": rsp("nuh uh, imma mention it again"),
    "You taste cold": rsp("yeah, cus im not hot"),
    "oh thank goodness. that makes me feel better about this not being an answer": rsp("what the hell does this have to do with homosexuality?"),
    "veggies": rsp("eww, i only like froot"),
    "I'm not from Canada I just wanted to be different": rsp("LOLOLOLOL TWINS"),
    "like pushing a hotdog thru a audio jack": rsp("thats how tight ma ass is"),
    "My wife may not be happy but I will be": rsp("we know bonkles, and that is nothing to be pround of"),
}
