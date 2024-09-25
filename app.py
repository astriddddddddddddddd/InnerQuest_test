from flask import Flask, render_template, session, jsonify, request      
import uuid
import textwrap
#import google.generativeai as genai
import usersQuestions as userq
import random                                 
import os
import openai

#gemini
#genai.configure(api_key='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
')

# OpenAI
openai.api_key = "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"


# Definition
cagry_prompt = {}
cagry_prompt["Bad"] = "Bored: Feeling indifferent or apathetic due to a lack of interest or stimulation." \
                  "Busy: Feeling pressured or rushed due to having many tasks or commitments to manage." \
                  "Stressed: Feeling overwhelmed or out of control due to excessive demands or challenges." \
                  "Tired: Feeling sleepy or unfocused due to a lack of rest or mental fatigue."                
cagry_prompt["Surprised"] = "Startled: Feeling suddenly surprised or alarmed due to an unexpected event." \
                  "Confused: Feeling unable to think clearly or understand something." \
                  "Amazed: Feeling overwhelming surprise or wonder." \
                  "Excited: Feeling enthusiastic and eager about something."
cagry_prompt["Happy"] = "Playful: Feeling light-hearted and full of fun often involving spontaneous and lively behavior." \
                  "Content: Feeling satisfied and at ease with one's situation." \
                  "Interested: Feeling curiosity and attentiveness towards something or someone." \
                  "Proud: Feeling deep pleasure or satisfaction as a result of one's own achievements, qualities or possessions." \
                  "Accepted: Feeling recognized and valued by others often contributing to a sense of belonging." \
                  "Powerful: Feeling strong and capable often with the ability to influence or control situations." \
                  "Peaceful: Feeling calm and serene free from disturbance or conflict." \
                  "Trusting: Feeling confident in the reliability, truth or ability of someone or something." \
                  "Optimistic: Feeling hopeful and confident about the future."                  
cagry_prompt["Sad"] =  "Lonely: Feeling isolated and lacking companionship." \
                  "Vulnerable: Feeling susceptible to harm or emotional injury." \
                  "Despair: Feeling a complete loss of hope or confidence." \
                  "Guilty: Feeling responsible for wrongdoing or offense." \
                  "Depressed: Feeling of severe despondency and dejection." \
                  "Hurt: Feeling emotional pain or distress."
cagry_prompt["Disgusted"] = "Disapproving: Expressing or feeling negative judgment or disapproval towards someone or something." \
                  "Disappointed: Feeling let down or disillusioned by unmet expectations or outcomes." \
                  "Awful: Extremely unpleasant or disagreeable; causing a feeling of dismay or horror." \
                  "Repelled: Feeling a strong aversion or disgust towards something or someone."
cagry_prompt["Angry"] = "Let-down: Feeling disappointed or betrayed by someone or something." \
                  "Humiliated: Feeling embarrassed or ashamed by being belittled or degraded." \
                  "Bitter: Feeling resentful or unhappy due to unfair treatment or disappointment." \
                  "Mad: Feeling angry or upset." \
                  "Aggressive: Feeling hostile or confrontational." \
                  "Frustrated: Feeling annoyed or discouraged due to obstacles or lack of progress." \
                  "Distant: Feeling emotionally or physically separated from others." \
                  "Critical: Expressing disapproval or judgment towards someone or something."
cagry_prompt["Fearful"] = "Scared: Feeling fear or apprehension about something." \
                  "Anxious: Feeling worried, nervous or uneasy about something with an uncertain outcome." \
                  "Insecure: Feeling uncertain or lacking confidence in oneself or one's abilities." \
                  "Weak: Lacking in strength or power either physically or emotionally." \
                  "Rejected: Feeling dismissed or excluded by others." \
                  "Threatened: Feeling in danger or at risk of harm or loss."

# html direction
cagry_html = {}
cagry_html["Bad"] = "bad.html"
cagry_html["Surprised"] = "surprised.html"
cagry_html["Happy"] = "happy.html"
cagry_html["Sad"] = "sad.html" 
cagry_html["Disgusted"] = "disgusted.html"
cagry_html["Angry"] = "angry.html"
cagry_html["Fearful"] = "fearful.html"  

#Subcategory
cagry_sub = {}

# bad_array
cagry_sub["Bad"] = {}
cagry_sub["Bad"]["Bored"] = ["Bored", "Feeling indifferent or apathetic due to a lack of interest or stimulation.", "bored.png", 
                             "\"Boredom is the feeling that everything is a waste of time; serenity, that nothing is.\" — Thomas Szasz",
                             "\"The cure for boredom is curiosity. There is no cure for curiosity.\" — Dorothy Parker"]
cagry_sub["Bad"]["Busy"] = ["Busy", "Feeling pressured or rushed due to having many tasks or commitments to manage.", "busy.png", 
                            "\"Take a rest. A field that has rested yields a beautiful crop.\" — Ovid",
                            "\"Just to be spontaneous and free is life's biggest luxury and privilege when life is so busy.\" — Morten Harket"]
cagry_sub["Bad"]["Stressed"] = ["Stressed", "Feeling overwhelmed or out of control due to excessive demands or challenges.", "stressed.png", 
                                 "\"Within you, there is a stillness and a sanctuary to which you can retreat at any time and be yourself.\" — Hermann Hesse",
                                 "\"Stress acts as an accelerator: it will push you either forward or backward, but you choose which direction.\" — Chelsea Erieau"]
cagry_sub["Bad"]["Tired"] = ["Tired", "Feeling sleepy or unfocused due to a lack of rest or mental fatigue.", "tired.png", 
                             "\"Rest and self-care are so important. When you take time to replenish your spirit, it allows you to serve others from the overflow. You cannot serve from an empty vessel.\" — Eleanor Brownn",
                             "\"Nobody’s perfect, so give yourself credit for everything you’re doing right, and be kind to yourself when you struggle.\" — Lori Deschene"]

# happy_array
cagry_sub["Happy"] = {}
cagry_sub["Happy"]["Playful"] = ["Playful", "Feeling light-hearted and full of fun often involving spontaneous and lively behavior.", "playful.png", 
                                 "\"We don’t stop playing because we grow old; we grow old because we stop playing.\" — George Bernard Shaw",
                                 "\"In every real man a child is hidden that wants to play.\" — Friedrich Nietzsche"]
cagry_sub["Happy"]["Content"] = ["Content", "Feeling satisfied and at ease with one's situation.", "content.png", 
                                  "\"Happiness consists not in having much, but in being content with little.\" — Marguerite Gardiner",
                                  "\"He is the richest who is content with the least, for content is the wealth of nature.\" — Socrates"]
cagry_sub["Happy"]["Interested"] = ["Interested", "Feeling curiosity and attentiveness towards something or someone.", "interested.png", 
                                     "\"The important thing is not to stop questioning. Curiosity has its own reason for existing.\" — Albert Einstein",
                                     "\"The cure for boredom is curiosity. There is no cure for curiosity.\" — Dorothy Parker"]
cagry_sub["Happy"]["Proud"] = ["Proud", "Feeling deep pleasure or satisfaction as a result of one's own achievements, qualities or possessions.", "proud.png", 
                                "\"Self-respect is the fruit of discipline; the sense of dignity grows with the ability to say no to oneself.\" — Abraham Joshua Heschel",
                                "\"Take pride in how far you’ve come and have faith in how far you can go.\" — Christian Larson"]
cagry_sub["Happy"]["Accepted"] = ["Accepted", "Feeling recognized and valued by others often contributing to a sense of belonging.", "accepted.png", 
                                   "\"The greatest gift you can give yourself is the permission to be who you truly are.\" — Anonymous",
                                   "\"Acceptance is not love. You love a person because he or she has lovable traits, but you accept everybody just because they’re alive and human.\" — Albert Ellis"]
cagry_sub["Happy"]["Powerful"] = ["Powerful", "Feeling strong and capable often with the ability to influence or control situations.", "powerful.png", 
                                   "\"You are more powerful than you know; you are beautiful just as you are.\" — Melissa Etheridge",
                                   "\"What lies behind us and what lies before us are tiny matters compared to what lies within us.\" — Ralph Waldo Emerson"]
cagry_sub["Happy"]["Peaceful"] = ["Peaceful", "Feeling calm and serene free from disturbance or conflict.", "peaceful.png", 
                                   "\"When you find peace within yourself, you become the kind of person who can live at peace with others.\" — Peace Pilgrim",
                                   "\"Nothing can bring you peace but yourself.\" — Ralph Waldo Emerson"]
cagry_sub["Happy"]["Trusting"] = ["Trusting", "Feeling confident in the reliability, truth or ability of someone or something.", "trusting.png", 
                                   "\"Trust yourself. You know more than you think you do.\" — Benjamin Spock",
                                   "\"Trust is the glue of life. It’s the most essential ingredient in effective communication. It’s the foundational principle that holds all relationships.\" — Stephen R. Covey"]
cagry_sub["Happy"]["Optimistic"] = ["Optimistic", "Feeling hopeful and confident about the future.", "optimistic.png", 
                                     "\"The best way to predict the future is to create it.\" — Peter Drucker",
                                     "\"Optimism is the faith that leads to achievement. Nothing can be done without hope and confidence.\" — Helen Keller"]

# surprised_array
cagry_sub["Surprised"] = {}
cagry_sub["Surprised"]["Startled"] = ["Startled", "Feeling suddenly surprised or alarmed due to an unexpected event.", "startled.png", 
                                      "\"The greatest weapon against stress is our ability to choose one thought over another.\" — William James",
                                      "\"When something bad happens, you have three choices. You can either let it define you, let it destroy you, or let it strengthen you.\" — Anonymous"]
cagry_sub["Surprised"]["Confused"] = ["Confused", "Feeling unable to think clearly or understand something.", "confused.png", 
                                       "\"Sometimes, when you're in a dark place, you think you've been buried, but actually you've been planted.\" — Christine Caine",
                                       "\"Not until we are lost do we begin to understand ourselves.\" — Henry David Thoreau"]
cagry_sub["Surprised"]["Amazed"] = ["Amazed", "Feeling overwhelming surprise or wonder.", "amazed.png", 
                                    "\"He who can no longer pause to wonder and stand rapt in awe, is as good as dead; his eyes are closed.\" — Albert Einstein",
                                    "\"Be grateful for small things, big things, and everything in between. Count your blessings, not your problems.\" — Anonymous"]
cagry_sub["Surprised"]["Excited"] = ["Excited", "Feeling enthusiastic and eager about something.", "excited.png", 
                                      "\"Excitement is the more practical synonym for happiness, and it is precisely what you should strive to chase. It is the cure-all.\" — Tim Ferriss",
                                      "\"The only way to make sense out of change is to plunge into it, move with it, and join the dance.\" — Alan Watts"]

# fearful_array
cagry_sub["Fearful"] = {}
cagry_sub["Fearful"]["Scared"] = ["Scared", "Feeling fear or apprehension about something.", "scared.png", 
                                  "\"Courage is not the absence of fear, but the triumph over it.\" — Nelson Mandela",
                                  "\"Fear is the path to the dark side. Fear leads to anger; anger leads to hate; hate leads to suffering.\" — Yoda"]
cagry_sub["Fearful"]["Anxious"] = ["Anxious", "Feeling worried, nervous or uneasy about something with an uncertain outcome.", "anxious.png", 
                                   "\"Anxiety does not empty tomorrow of its sorrows, but only empties today of its strength.\" — Charles Spurgeon",
                                   "\"Worrying is carrying tomorrow’s load with today’s strength – carrying two days at once. It is moving into tomorrow ahead of time.\" — Corrie Ten Boom"]
cagry_sub["Fearful"]["Insecure"] = ["Insecure", "Feeling uncertain or lacking confidence in oneself or one's abilities.", "insecure.png", 
                                     "\"You are imperfect, permanently and inevitably flawed. And you are beautiful.\" — Amy Bloom",
                                     "\"Remember, you have been criticizing yourself for years and it hasn’t worked. Try approving yourself and see what happens.\" — Louise Hay"]
cagry_sub["Fearful"]["Weak"] = ["Weak", "Lacking in strength or power either physically or emotionally.", "weak.png", 
                                 "\"Out of suffering have emerged the strongest souls; the most massive characters are seared with scars.\" — Khalil Gibran",
                                 "\"The world breaks everyone, and afterward, some are strong at the broken places.\" — Ernest Hemingway"]
cagry_sub["Fearful"]["Rejected"] = ["Rejected", "Feeling dismissed or excluded by others.", "rejected.png", 
                                     "\"Every rejection is incremental payment on your dues that in some way will be translated back into your work.\" — James Lee Burke",
                                     "\"Often, what feels like the end of the world is really a challenging pathway to a far better place.\" — Karen Salmansohn"]
cagry_sub["Fearful"]["Threatened"] = ["Threatened", "Feeling in danger or at risk of harm or loss.", "threatened.png", 
                                      "\"You gain strength, courage, and confidence by every experience in which you really stop to look fear in the face.\" — Eleanor Roosevelt",
                                      "\"When you know yourself, you are empowered. When you accept yourself, you are invincible.\" — Tina Lifford"]

# disgusted_array
cagry_sub["Disgusted"] = {}
cagry_sub["Disgusted"]["Disapproving"] = ["Disapproving", "Expressing or feeling negative judgment or disapproval towards someone or something.", "disapproving.png", 
                                         "\"Do not judge my story by the chapter you walked in on.\" — Anonymous",
                                         "\"Be curious, not judgmental.\" — Walt Whitman"]
cagry_sub["Disgusted"]["Disappointed"] = ["Disappointed", "Feeling let down or disillusioned by unmet expectations or outcomes.", "disappointed.png", 
                                          "\"When one door closes, another opens; but we often look so long and so regretfully upon the closed door that we do not see the one which has opened for us.\" — Alexander Graham Bell",
                                          "\"Blessed is he who expects nothing, for he shall never be disappointed.\" — Alexander Pope"]
cagry_sub["Disgusted"]["Awful"] = ["Awful", "Extremely unpleasant or disagreeable; causing a feeling of dismay or horror.", "awful.png", 
                                    "\"When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.\" — Henry Ford",
                                    "\"Pain is inevitable. Suffering is optional.\" — Haruki Murakami"]
cagry_sub["Disgusted"]["Repelled"] = ["Repelled", "Feeling a strong aversion or disgust towards something or someone.", "repelled.png", 
                                      "\"Your task is not to seek for love, but merely to seek and find all the barriers within yourself that you have built against it.\" — Rumi",
                                      "\"Turn your face to the sun and the shadows fall behind you.\" — Maori Proverb"]

# angry_array
cagry_sub["Angry"] = {}
cagry_sub["Angry"]["Let-down"] = ["Let-down", "Feeling disappointed or betrayed by someone or something.", "let-down.png", 
                                  "\"Disappointments are often blessings in disguise, leading you to something better.\" — Dalai Lama",
                                  "\"Trust that life's setbacks are preparing you for greater things.\" — Anonymous"]
cagry_sub["Angry"]["Humiliated"] = ["Humiliated", "Feeling embarrassed or ashamed by being belittled or degraded.", "humiliated.png", 
                                    "\"Letting go of the past allows you to discover your true self.\" — Deepak Chopra",
                                    "\"If you are never scared, embarrassed, or hurt, it means you never take chances.\" — Julia Soul"]
cagry_sub["Angry"]["Bitter"] = ["Bitter", "Feeling resentful or unhappy due to unfair treatment or disappointment.", "bitter.png", 
                                "\"Don’t be so bitter about a bad experience from your past that you miss the opportunities in front of you.\" — Nelson Mandela",
                                "\"Hurt gives way to bitterness, bitterness to anger. Travel too far that road and the way is lost.\" — Terry Brooks"]
cagry_sub["Angry"]["Mad"] = ["Mad", "Feeling angry or upset.", "mad.png", 
                             "\"Anger helps strengthen out a problem like a fan helps straighten out a pile of papers.\" — Susan Mancotte",
                             "\"Channel your energy into building a positive and loving life.\" — Lawrence G. Lovasik"]
cagry_sub["Angry"]["Aggressive"] = ["Aggressive", "Feeling hostile or confrontational.", "aggressive.png", 
                                    "\"Holding on to anger is like grasping a hot coal with the intent of throwing it at someone else; you are the one who gets burned.\" — Buddha",
                                    "\"True victory lies in choosing peace over conflict.\" — Sun Tzu"]
cagry_sub["Angry"]["Frustrated"] = ["Frustrated", "Feeling annoyed or discouraged due to obstacles or lack of progress.", "frustrated.png", 
                                    "\"Embrace frustration as a stepping stone to success and growth.\" — Bo Bennett",
                                    "\"Release your stress and find peace in the flow of life.\" — Steve Maraboli"]
cagry_sub["Angry"]["Distant"] = ["Distant", "Feeling emotionally or physically separated from others.", "distant.png", 
                                 "\"Embrace resistance as a tool to build strong character and resilience.\" — Arnold Schwarzenegger",
                                 "\"Life is not about waiting for the storms to pass. It’s about learning how to dance in the rain.\" — Vivian Greene"]
cagry_sub["Angry"]["Critical"] = ["Critical", "Expressing disapproval or judgment towards someone or something.", "critical.png", 
                                  "\"Choosing kindness over judgment transforms both you and the world around you.\" — Wayne Dyer",
                                  "\"Don’t be distracted by criticism. Remember, the only taste of success some people have is when they take a bite out of you.\" — Zig Ziglar"]

# sad_array
cagry_sub["Sad"] = {}
cagry_sub["Sad"]["Lonely"] = ["Lonely", "Feeling isolated and lacking companionship.", "lonely.png", 
                               "\"The soul that sees beauty may sometimes walk alone.\" — Johann Wolfgang von Goethe",
                               "\"Loneliness and the feeling of being unwanted is the most terrible poverty.\" — Mother Teresa"]
cagry_sub["Sad"]["Vulnerable"] = ["Vulnerable", "Feeling susceptible to harm or emotional injury.", "vulnerable.png", 
                                  "\"Vulnerability is not winning or losing; it’s having the courage to show up and be seen when we have no control over the outcome.\" — Brené Brown",
                                  "\"Being vulnerable is the only way to allow your heart to feel true pleasure.\" — Bob Marley"]
cagry_sub["Sad"]["Despair"] = ["Despair", "Feeling a complete loss of hope or confidence.", "despair.png", 
                                "\"Never lose hope. Storms make people stronger and never last forever.\" — Roy T. Bennett",
                                "\"In the middle of difficulty lies opportunity.\" — Albert Einstein"]
cagry_sub["Sad"]["Guilty"] = ["Guilty", "Feeling responsible for wrongdoing or offense.", "guilty.png", 
                               "\"Guilt is not a response to anger; it is a response to one’s own actions or lack of action.\" — Audre Lorde",
                               "\"The greatest glory in living lies not in never falling, but in rising every time we fall.\" — Nelson Mandela"]
cagry_sub["Sad"]["Depressed"] = ["Depressed", "Feeling of severe despondency and dejection.", "depressed.png", 
                                  "\"Even the darkest night will end, and the sun will rise.\" — Victor Hugo",
                                  "\"Faith is the bird that feels the light when the dawn is still dark.\" — Rabindranath Tagore"]
cagry_sub["Sad"]["Hurt"] = ["Hurt", "Feeling emotional pain or distress.", "hurt.png", 
                            "\"Our wounds are often the openings into the best and most beautiful part of us.\" — David Richo",
                            "\"The wound is where the Light enters you.\" — Rumi"]

qnum=0

'''
def get_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
#   response = model.generate_content(prompt)
    response = model.generate_content(
    prompt,
    safety_settings={
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL' : 'BLOCK_NONE',
        'DANGEROUS' : 'BLOCK_NONE'
    })
    try:
        print(response.text)
    except:
        return "Security Issue. Please SKIP"
    return response.text
'''

#OpenAI
def get_response(prompt):
    response = client.chat.completions.create(
#      model="gpt-4",    
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt},
      ]
    )
    #print(response.json())
    #print(response.choices[0].message.content)
    return response.choices[0].message.content
    
       
app = Flask(__name__)
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
secret_key = os.getenv('SECRET_KEY')
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
     client_uuid = str(uuid.uuid4())
     userq.add_user(client_uuid)
     return render_template('index.html', client_uuid=client_uuid)

@app.route('/InnerQuestion/<cagry>/<cuuid>')
def innerQuest(cagry,cuuid):
     global qnum
     print("category:"+cagry)
     prompt=  "Create one yes no question without actually using the words in the following description to help to identify which of the following categories they fall in." + cagry_prompt[cagry]
     try:
        question = get_response(prompt)
     except Exception as e:
        print(f"API Error: {e}")
        print("Prompt:")
        print(prompt)
        question="System error! Please press SKIP!"
     print(question)
     userq.clear_user_questions(cuuid)
     userq.add_user_question(cuuid,question)
     qnum=1
     return render_template('InnerQuest Qs.html', question=question,category=cagry,client_uuid=cuuid,qnum=str(qnum))
     
@app.route('/InnerQuestion/<cagry>/<cuuid>/<resp>')
def innerQuest_2(cagry,cuuid,resp):
    global qnum
    print("category:"+cagry+"  resp:"+resp)
    if resp == "yes":
        userq.add_user_question(cuuid,"Yes\n")
    elif resp == "no":
        userq.add_user_question(cuuid,"No\n")
    elif resp == "maybe":
        userq.add_user_question(cuuid,"Maybe\n")
    elif resp == "back":
        if qnum > 1:
            userq.delete_last_user_question(cuuid)
            userq.delete_last_user_question(cuuid)
            qnum=qnum-1
        question=userq.return_last_user_question(cuuid)            
        return render_template('InnerQuest Qs.html', question=question,category=cagry,client_uuid=cuuid,qnum=str(qnum))
    if userq.get_user_question_count(cuuid) >= 20:
        prompt= userq.return_user_questions(cuuid) + "According to the responses above, which category is the person in? Without add additional wordings, just the one word for the category Respond me in english, out of these categories." + cagry_prompt[cagry]
        result=get_response(prompt)
        result=result.split(' ')[0]
        print("result:")
        print(result)
        userq.delete_user(cuuid)
        if result not in cagry_sub[cagry]:
            return ("The result is not the the categories :" + result)
        quoteNum = random.choice([3, 4])
        print(f"quote select number:{quoteNum}")
        return render_template(cagry_html[cagry], mood=cagry_sub[cagry][result][0],desc=cagry_sub[cagry][result][1],imgName=cagry_sub[cagry][result][2], quote=cagry_sub[cagry][result][quoteNum]) 
    prompt= userq.return_user_questions(cuuid)+ "According to the responses above, can you make one more yes-no question that will lead to more accurate analysis of the category the person falls in? Without any additional wordings, just the question." 
    try:
        question = get_response(prompt)   
    except Exception as e:
        print(f"API Error: {e}")
        print("Prompt:")
        print(prompt)
        question="System error! Please press SKIP!"
    print(question)
    userq.add_user_question(cuuid,question)
    qnum=qnum+1
    return render_template('InnerQuest Qs.html', question=question,category=cagry,client_uuid=cuuid,qnum=str(qnum))     
     
if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
