
import pygame


era_dialogues = {

    "Museum": [
        "..First night shift alone.",
        "..No backup, no walkthroughs..just me.",
        "This place used to be smaller ... just a gallery.",
        "Now it’s a full museum ... every era, every style...",
        "..He really built all of this from scratch.",
        "..You really trusted me with this, huh?",
        "I don’t even know where to start..",
        "You made this place feel alive.",
        "..Right now, it just feels empty.",
        "scene 2 starts here"
    ],

    "1920s": [
        "...Whoa-",
        "..This is definitely not the museum anymore.",
        "Clothes.. hairstyles.. even the way they walk..",
        "..1920s.It actually worked.",
        "I just time traveled.. because someone stole clothes.",
        "..Alright. Focus.",
        "If the thief came here..",
        "..then the item has to be here too.",
        "And if it doesn’t belong in this era..",
        "..it should stand out."
    ],

    "1950s": [
        "—Okay.. yeah.. still not used to that.",
        "..This isn’t just a street..",
        "..It’s a gallery.",
        "So this is what it used to be like..",
        "Before it became a full museum.",
        "Alright."
    ],

    "1960s": [
        "—Okay.. that one definitely hits harder.",
        "..Woah.",
        "Everything’s louder.. brighter..",
        "..Yeah. This has to be the 60s.",
        "Styles are more expressive.. less rigid..",
        "..More freedom.",
        "Alright.",
        "Find what doesn’t belong."
    ],

    "1980s": [
        "—Okay.. yeah, that’s definitely getting stronger.",
        "..Woah.",
        "Everything’s.. louder.",
        "Bigger. Flashier.",
        "And this place..",
        "..It’s not just a gallery anymore.",
        "It’s becoming something bigger.",
        "Alright.",
        "One more step closer."
    ],

    "1990s": [
        "..Alright.",
        "That felt.. different.",
        "..This is it.",
        "The museum.",
        "No longer just a gallery..",
        "He finished what he started.",
        "One last item.",
        "Then I find her."
    ]
}

# NPC DATA
dialogue_data = {
    # =====================
    # Museum NPC 0: Manager
    # =====================
    ("Museum", 13, 6): {
        "speaker": "Manager",
        "dialogue": [
            {"speaker": "MANAGER", "text": "I heard something break—what happened here?!"},
            {"speaker": "PLAYER", "text": "I don’t know—I just got here and found it like this."},
            {"speaker": "MANAGER", "text": "..The display.."},
            {"speaker": "MANAGER", "text": "The artifacts.."},
            {"speaker": "PLAYER", "text": "What about them?"},
            {"speaker": "MANAGER", "text": "They’re gone."},
            {"speaker": "PLAYER", "text": "..Gone?"},
            {"speaker": "MANAGER", "text": "Several items. From different sections."},
            {"speaker": "PLAYER", "text": "Different sections..?"},
            {"speaker": "MANAGER", "text": "Different eras."},
            {"speaker": "PLAYER", "text": "So whoever did this.. knew exactly what they were taking."},
            {"speaker": "MANAGER", "text": "Yes."},
            {"speaker": "MANAGER", "text": "This wasn’t random. This was planned."},
            {"speaker": "DEVICE REALIZATION", "text": "???"},
            {"speaker": "MANAGER", "text": "..Where did you get that?"},
            {"speaker": "PLAYER", "text": "It was on the floor. Right next to the case."},
            {"speaker": "MANAGER", "text": "..Let me see."},
            {"speaker": "MANAGER", "text": "This isn’t from the collection."},
            {"speaker": "PLAYER", "text": "That’s what I said."},
            {"speaker": "MANAGER", "text": "And it doesn’t look modern either..."},
            {"speaker": "PLAYER", "text": "..So what is it?"},
            {"speaker": "MANAGER", "text": "I think.."},
            {"speaker": "MANAGER", "text": "This is how they did it."},
            {"speaker": "PLAYER", "text": "..Did what?"},
            {"speaker": "MANAGER", "text": "Moved through time."},
            {"speaker": "PLAYER", "text": "..You’re serious?"},
            {"speaker": "MANAGER", "text": "The items taken—they’re all from different decades."},
            {"speaker": "MANAGER", "text": "If someone had access to something like this.."},
            {"speaker": "PLAYER", "text": "..They wouldn’t need to steal everything at once."},
            {"speaker": "MANAGER", "text": "They could take them from anywhere. Any time."},
            {"speaker": "PASSING THE RESPONSIBILITY", "text": "???"},
            {"speaker": "MANAGER", "text": "You’re his grandson."},
            {"speaker": "PLAYER", "text": "That doesn’t mean I understand any of this."},
            {"speaker": "MANAGER", "text": "Your grandfather didn’t just collect clothes."},
            {"speaker": "MANAGER", "text": "He started with a small gallery.."},
            {"speaker": "MANAGER", "text": "And turned it into a living timeline of fashion."},
            {"speaker": "PLAYER", "text": "I know what he built."},
            {"speaker": "MANAGER", "text": "He studied every era. Lived through them, in his own way."},
            {"speaker": "MANAGER", "text": "And he taught you, didn’t he?"},
            {"speaker": "PLAYER", "text": "..Not like that."},
            {"speaker": "PLAYER", "text": "I just helped around. Watched. Listened."},
            {"speaker": "MANAGER", "text": "Then you know more than anyone else here."},
            {"speaker": "PLAYER", "text": "I’m just the night guard."},
            {"speaker": "MANAGER", "text": "No."},
            {"speaker": "MANAGER", "text": "You’re the only one who can follow this."},
            {"speaker": "THE MISSION", "text": "=>"},
            {"speaker": "PLAYER", "text": "...Follow it where?"},
            {"speaker": "MANAGER", "text": "Wherever that thing leads."},
            {"speaker": "PLAYER", "text": "You want me to use this?"},
            {"speaker": "MANAGER", "text": "If the thief used it to move through time.."},
            {"speaker": "PLAYER", "text": "..Then I can use it to track them."},
            {"speaker": "MANAGER", "text": "Exactly."},
            {"speaker": "PLAYER", "text": "This sounds insane."},
            {"speaker": "MANAGER", "text": "Maybe it is."},
            {"speaker": "MANAGER", "text": "But those items matter."},
            {"speaker": "MANAGER", "text": "They’re not just displays."},
            {"speaker": "MANAGER", "text": "They’re pieces of history your grandfather preserved."},
            {"speaker": "PLAYER", "text": "..So whoever did this.."},
            {"speaker": "PLAYER", "text": "They’re not just stealing."},
            {"speaker": "PLAYER", "text": "They’re tearing the story apart."},
            {"speaker": "ACTIVATION", "text": "===>"},
            {"speaker": "DEVICE", "text": "Temporal system activated."},
            {"speaker": "PLAYER", "text": "..Yeah, of course it talks."},
            {"speaker": "DEVICE", "text": "Select destination era."},
            {"speaker": "PLAYER", "text": "..1920s.."},
            {"speaker": "PLAYER", "text": "Guess we start at the beginning."},
            {"speaker": "PLAYER", "text": "..Don’t let me mess this up, grandpa."}
        ],
    },


    # =========================
    # 1920s NPC 1: Elegant Woman
    # =========================
    "elegant_woman": {
        "dialogue": [
            {"speaker": "ELEGANT WOMAN", "text": "Well now, you look like you've walked straight out of a different world."},
            {"speaker": "PLAYER", "text": "..Something like that."},
            {"speaker": "ELEGANT WOMAN", "text": "That outfit.. I don't think I've seen anything like it."},
            {"speaker": "PLAYER", "text": "I could say the same."},
            {"speaker": "ELEGANT WOMAN", "text": "Fair enough."},
            {"speaker": "ELEGANT WOMAN", "text": "You're not from around here, are you?"},
            {"speaker": "PLAYER", "text": "..I'm just passing through."},
            {"speaker": "ELEGANT WOMAN", "text": "Mmm.. mysterious. I like it."},
            {"speaker": "PLAYER", "text": "Have you seen anything.. unusual around here?"},
            {"speaker": "ELEGANT WOMAN", "text": "Unusual? In this city? Always."},
            {"speaker": "PLAYER", "text": "I mean something that doesn't belong."},
            {"speaker": "ELEGANT WOMAN", "text": "..Now that you mention it.."},
            {"speaker": "PLAYER", "text": "What?"},
            {"speaker": "ELEGANT WOMAN", "text": "There was a girl earlier."},
            {"speaker": "PLAYER", "text": "What about her?"},
            {"speaker": "ELEGANT WOMAN", "text": "She didn't quite fit in."},
            {"speaker": "PLAYER", "text": "How so?"},
            {"speaker": "ELEGANT WOMAN", "text": "She looked.. restless. Eyes darting everywhere."},
            {"speaker": "ELEGANT WOMAN", "text": "Like she was hiding something. Or planning something."},
            {"speaker": "PLAYER", "text": "Did you notice anything else?"},
            {"speaker": "ELEGANT WOMAN", "text": "..Her shoes."},
            {"speaker": "PLAYER", "text": "Shoes?"},
            {"speaker": "ELEGANT WOMAN", "text": "They were.. strange."},
            {"speaker": "ELEGANT WOMAN", "text": "Tall. White. Sleek."},
            {"speaker": "ELEGANT WOMAN", "text": "Not like anything we wear."},
            {"speaker": "CLUE", "text": "Clue discovered: Go-Go Boots."},
            {"speaker": "PLAYER", "text": "..That has to be it."},
            {"speaker": "ELEGANT WOMAN", "text": "If you find her, do let me know. I adore a bit of drama."},
            {"speaker": "PLAYER", "text": "I'll keep that in mind."}
        ],
        "quest": "clue_gogo_boots",
        "clue": "gogo_boots"
    },

    # =========================
    # 1920s NPC 2: Old Tailor
    # =========================
    "old_tailor": {
        "dialogue": [
            {"speaker": "OLD TAILOR", "text": "..Hmm."},
            {"speaker": "PLAYER", "text": "..Excuse me?"},
            {"speaker": "OLD TAILOR", "text": "Hold still."},
            {"speaker": "PLAYER", "text": "...What?"},
            {"speaker": "OLD TAILOR", "text": "..That stitching. That cut."},
            {"speaker": "OLD TAILOR", "text": "You remind me of someone."},
            {"speaker": "PLAYER", "text": "I do?"},
            {"speaker": "OLD TAILOR", "text": "Yes.. a young man."},
            {"speaker": "OLD TAILOR", "text": "Always asking questions about garments.. about time."},
            {"speaker": "PLAYER", "text": "..Time?"},
            {"speaker": "OLD TAILOR", "text": "He said clothing tells stories."},
            {"speaker": "OLD TAILOR", "text": "Not just of people.. but of eras."},
            {"speaker": "PLAYER", "text": "..My grandfather."},
            {"speaker": "OLD TAILOR", "text": "Ah. So you know him."},
            {"speaker": "PLAYER", "text": "He.. used to talk like that."},
            {"speaker": "OLD TAILOR", "text": "He had an eye for detail."},
            {"speaker": "OLD TAILOR", "text": "And a habit of noticing things others ignored."},
            {"speaker": "OLD TAILOR", "text": "If you're looking for something.."},
            {"speaker": "OLD TAILOR", "text": "Don't just look at what fits in."},
            {"speaker": "OLD TAILOR", "text": "Look for what doesn't."},
            {"speaker": "PLAYER", "text": "..Yeah."},
            {"speaker": "PLAYER", "text": "That sounds like him."}
        ],
        "quest": "old_tailor_hint"
    },


    "gallery_host": {
        "dialogue": [
            {"speaker": "GALLERY HOST", "text": "Well, you look a little out of place."},
            {"speaker": "PLAYER", "text": "..That obvious?"},
            {"speaker": "GALLERY HOST", "text": "Just a little."},
            {"speaker": "GALLERY HOST", "text": "Here for the exhibition?"},
            {"speaker": "PLAYER", "text": "..Something like that."},
            {"speaker": "PLAYER", "text": "I’m actually looking for something unusual."},
            {"speaker": "GALLERY HOST", "text": "Oh? In a place full of fashion?"},
            {"speaker": "PLAYER", "text": "Something that doesn’t belong to this time."},
            {"speaker": "GALLERY HOST", "text": "..You know.."},
            {"speaker": "PLAYER", "text": "What?"},
            {"speaker": "GALLERY HOST", "text": "There was a girl earlier."},
            {"speaker": "PLAYER", "text": "..A girl?"},
            {"speaker": "GALLERY HOST", "text": "Yes. Didn’t seem interested in the displays."},
            {"speaker": "GALLERY HOST", "text": "She kept looking around instead.. like she was searching for something."},
            {"speaker": "PLAYER", "text": "Did anything stand out about her?"},
            {"speaker": "GALLERY HOST", "text": "..Her pants."},
            {"speaker": "PLAYER", "text": "What about them?"},
            {"speaker": "GALLERY HOST", "text": "They didn’t match the rest of the era."},
            {"speaker": "GALLERY HOST", "text": "Faded in patches.. uneven coloring."},
            {"speaker": "GALLERY HOST", "text": "Almost like they were.. damaged on purpose."},
            {"speaker": "CLUE", "text": "Clue discovered: Acid Wash Denim"},
            {"speaker": "PLAYER", "text": "..That’s it."},
            {"speaker": "GALLERY HOST", "text": "She wandered deeper into the gallery after that."},
            {"speaker": "GALLERY HOST", "text": "Towards the back exhibits."},
        ],
        "quest": "clue_acid_wash_denim"
    },


    "fashion_enthusiast": {
        "dialogue": [
            {"speaker": "FASHION ENTHUSIAST", "text": "You’re staring."},
            {"speaker": "PLAYER", "text": "..That obvious?"},
            {"speaker": "FASHION ENTHUSIAST", "text": "In here? Yeah."},
            {"speaker": "FASHION ENTHUSIAST", "text": "And that outfit? Completely out of place."},
            {"speaker": "PLAYER", "text": "I get that a lot."},
            {"speaker": "PLAYER", "text": "I’m looking for something specific."},
            {"speaker": "FASHION ENTHUSIAST", "text": "Everyone is. What makes yours special?"},
            {"speaker": "PLAYER", "text": "It doesn’t belong in this era."},
            {"speaker": "FASHION ENTHUSIAST", "text": "..Now that’s interesting."},
            {"speaker": "FASHION ENTHUSIAST", "text": "There was someone like that earlier."},
            {"speaker": "PLAYER", "text": "A girl?"},
            {"speaker": "FASHION ENTHUSIAST", "text": "Yes."},
            {"speaker": "FASHION ENTHUSIAST", "text": "She didn’t blend in."},
            {"speaker": "PLAYER", "text": "How so?"},
            {"speaker": "FASHION ENTHUSIAST", "text": "Everything here is bold, intentional.."},
            {"speaker": "FASHION ENTHUSIAST", "text": "But she felt.. calculated."},
            {"speaker": "PLAYER", "text": "Did you notice what she was wearing?"},
            {"speaker": "FASHION ENTHUSIAST", "text": "..Red dress."},
            {"speaker": "PLAYER", "text": "Red?."},
            {"speaker": "FASHION ENTHUSIAST", "text": "Bright. Hard to miss."},
            {"speaker": "FASHION ENTHUSIAST", "text": "And her hair—tied back."},
            {"speaker": "CLUE", "text": "Clue discovered: Red dress + ponytail"},
            {"speaker": "PLAYER", "text": "..That matches."},
            {"speaker": "FASHION ENTHUSIAST", "text": "But that’s not what stood out most."},
            {"speaker": "PLAYER", "text": "Then what?"},
            {"speaker": "NPC 1", "text": "She was holding something strange."},
            {"speaker": "PLAYER", "text": "What kind of item?"},
            {"speaker": "NPC 1", "text": "A shirt."},
            {"speaker": "NPC 1", "text": "Loose.. patterned.."},
            {"speaker": "NPC 1", "text": "Not fitted like anything here."},
            {"speaker": "CLUE", "text": "Clue discovered: Flannel Shirt"},
            {"speaker": "PLAYER", "text": "Where did she go?"},
            {"speaker": "NPC 1", "text": "Toward the back."},
            {"speaker": "NPC 1", "text": "Near the storage racks."},
        ],
        "quest": "clue_flannel_shirt"
    },

    # ===========================
    # 1960s NPC 4: Gallery Staff
    # ===========================
    "gallery_staff": {
        "dialogue": [
            {"speaker": "GALLERY STAFF", "text": "Careful with those racks."},
            {"speaker": "PLAYER", "text": "I won’t touch anything I shouldn’t."},
            {"speaker": "GALLERY STAFF", "text": "..You’re not browsing."},
            {"speaker": "PLAYER", "text": "No."},
            {"speaker": "PLAYER", "text": "I’m looking for something that doesn’t belong here."},
            {"speaker": "GALLERY STAFF", "text": "..Then you think like him."},
            {"speaker": "PLAYER", "text": "My grandfather."},
            {"speaker": "GALLERY STAFF", "text": "Yes."},
            {"speaker": "GALLERY STAFF", "text": "He always said.."},
            {"speaker": "GALLERY STAFF", "text": "Every era has its rhythm. The wrong piece breaks it."},
            {"speaker": "PLAYER", "text": "..That sounds like him."},
            {"speaker": "GALLERY STAFF", "text": "You’ve inherited that awareness."},
            {"speaker": "PLAYER", "text": "A girl came through here."},
            {"speaker": "GALLERY STAFF", "text": "She did."},
            {"speaker": "PLAYER", "text": "What was she carrying?"},
            {"speaker": "GALLERY STAFF", "text": "A shirt."},
            {"speaker": "GALLERY STAFF", "text": "Rough fabric. Checkered pattern."},
            {"speaker": "GALLERY STAFF", "text": "Doesn’t belong in this decade."},
            {"speaker": "PLAYER", "text": "Where is it now?"},
            {"speaker": "GALLERY STAFF", "text": "She tried to hide it among the racks."},
            {"speaker": "GALLERY STAFF", "text": "But it stands out.. if you know what to look for."},
        ],
    },

    # ============================
    # 1980s NPC 5: Fashion Curator
    # ============================
    "fashion_curator": {
        "dialogue": [
            {"speaker": "FASHION CURATOR", "text": "If you’re here to admire, don’t stand in front of the display."},
            {"speaker": "PLAYER", "text": "I’m not here to admire."},
            {"speaker": "FASHION CURATOR", "text": "..Clearly"},
            {"speaker": "FASHION CURATOR", "text": "You stand out more than the exhibits.."},
            {"speaker": "PLAYER", "text": "I’m looking for something that doesn’t belong here."},
            {"speaker": "FASHION CURATOR", "text": "..That’s a very specific request."},
            {"speaker": "FASHION CURATOR", "text": "There was someone like that earlier."},
            {"speaker": "PLAYER", "text": "A girl."},
            {"speaker": "FASHION CURATOR", "text": "Yes."},
            {"speaker": "FASHION CURATOR", "text": "She didn’t look at the displays the way others do."},
            {"speaker": "PLAYER", "text": "How did she look at them?"},
            {"speaker": "FASHION CURATOR", "text": "Like they were pieces on a board."},
            {"speaker": "FASHION CURATOR", "text": "Not art. Not history."},
            {"speaker": "FASHION CURATOR", "text": "..Moves."},
            {"speaker": "PLAYER", "text": "She’s planning something."},
            {"speaker": "FASHION CURATOR", "text": "She already has."},
            {"speaker": "PLAYER", "text": "What did she look like?"},
            {"speaker": "FASHION CURATOR", "text": "Red dress."},
            {"speaker": "FASHION CURATOR", "text": "Hair tied back."},
            {"speaker": "PLAYER", "text": "...Yeah."},
            {"speaker": "FASHION CURATOR", "text": "And her expression.."},
            {"speaker": "PLAYER", "text": "What about it?"},
            {"speaker": "FASHION CURATOR", "text": "Confident."},
            {"speaker": "FASHION CURATOR", "text": "Playful."},
            {"speaker": "FASHION CURATOR", "text": "But not harmless."},
            {"speaker": "CLUE", "text": "Clue discovered: Mischiveous Personality"},
            {"speaker": "PLAYER", "text": "..Mischievous."},
            {"speaker": "FASHION CURATOR", "text": "And her shoes-"},
            {"speaker": "PLAYER", "text": "Black?"},
            {"speaker": "FASHION CURATOR", "text": "So you’ve seen her too."},
            {"speaker": "PLAYER", "text": "What was she carrying?"},
            {"speaker": "FASHION CURATOR", "text": "A shirt"},
            {"speaker": "PLAYER", "text": "What kind?"},
            {"speaker": "FASHION CURATOR", "text": "Short-sleeved."},
            {"speaker": "FASHION CURATOR", "text": "Loose. Casual."},
            {"speaker": "FASHION CURATOR", "text": "Didn’t match anything here."},
            {"speaker": "CLUE", "text": "Clue discovered: Bowling Shirt"},
            {"speaker": "FASHION CURATOR", "text": "She went toward the archive section."},
        ],
        "quest": "clue_bowling_shirt"
    },

    # ===========================
    # 1980s NPC 6: Archive Staff
    # ===========================
    "archive_staff": {
        "dialogue": [
            {"speaker": "ARCHIVE STAFF", "text": "If you’re here to browse, you’re in the wrong section."},
            {"speaker": "PLAYER", "text": "I’m not browsing."},
            {"speaker": "ARCHIVE STAFF", "text": "..No. You’re searching."},
            {"speaker": "PLAYER", "text": "Yes."},
            {"speaker": "PLAYER", "text": "For something that doesn’t belong in this era."},
            {"speaker": "ARCHIVE STAFF", "text": "..Then you’ve learned from him."},
            {"speaker": "PLAYER", "text": "My grandfather."},
            {"speaker": "ARCHIVE STAFF", "text": "He’s the reason this place changed."},
            {"speaker": "ARCHIVE STAFF", "text": "From a gallery.. into a museum."},
            {"speaker": "PLAYER", "text": "..I can see that."},
            {"speaker": "ARCHIVE STAFF", "text": "He always said.."},
            {"speaker": "ARCHIVE STAFF", "text": "Time refines everything.. except what doesn’t belong."},
            {"speaker": "PLAYER", "text": "A girl came through here."},
            {"speaker": "ARCHIVE STAFF", "text": "She did."},
            {"speaker": "PLAYER", "text": "What was she carrying?"},
            {"speaker": "ARCHIVE STAFF", "text": "A shirt."},
            {"speaker": "ARCHIVE STAFF", "text": "Lightweight. Short sleeves."},
            {"speaker": "ARCHIVE STAFF", "text": "Too simple for this decade’s style."},
            {"speaker": "PLAYER", "text": "Do you know where is it now?"},
            {"speaker": "ARCHIVE STAFF", "text": "I'm quite unsure about that."},
            {"speaker": "PLAYER", "text": "Alright, thank you."},
            {"speaker": "ARCHIVE STAFF", "text": "Your welcome."},
        ],
    },

    # ==============================
    # 1990s NPC 6: Curator Assistant
    # ==============================
    "curator_assistant": {
        "dialogue": [
            {"speaker": "CURATOR ASSISTANT", "text": "Please don’t cross the marked lines."},
            {"speaker": "PLAYER", "text": "I won’t."},
            {"speaker": "CURATOR ASSISTANT", "text": "..You look like you’re searching for something."},
            {"speaker": "PLAYER", "text": "I am."},
            {"speaker": "PLAYER", "text": "Something that doesn’t belong in this era."},
            {"speaker": "CURATOR ASSISTANT", "text": "..Then you’re looking for the same thing she was."},
            {"speaker": "PLAYER", "text": "She?"},
            {"speaker": "CURATOR ASSISTANT", "text": "A girl."},
            {"speaker": "PLAYER", "text": "Red dress?"},
            {"speaker": "CURATOR ASSISTANT", "text": "..Yes."},
            {"speaker": "CURATOR ASSISTANT", "text": "She stood out immediately."},
            {"speaker": "PLAYER", "text": "What else?"},
            {"speaker": "CURATOR ASSISTANT", "text": "Hair tied back."},
            {"speaker": "CURATOR ASSISTANT", "text": "Black shoes."},
            {"speaker": "PLAYER", "text": "..That’s her."},
            {"speaker": "CURATOR ASSISTANT", "text": "She wasn’t here to admire anything."},
            {"speaker": "CURATOR ASSISTANT", "text": "She was looking for a place to hide something."},
            {"speaker": "PLAYER", "text": "What kind of item?"},
            {"speaker": "CURATOR ASSISTANT", "text": "A necklace."},
            {"speaker": "CURATOR ASSISTANT", "text": "Long. Elegant."},
            {"speaker": "CURATOR ASSISTANT", "text": "Didn’t match anything from this decade."},
            {"speaker": "CLUE", "text": "Clue discovered: Pearl Necklace"},
            {"speaker": "CURATOR ASSISTANT", "text": "She moved toward the deeper archive section."},
        ],
        "quest": "clue_pearl_necklace"
    },

    # =====================
    # 1990s NPC 7: Visitor
    # =====================
    "visitor": {
        "dialogue": [
            {"speaker": "VISITOR", "text": "You’re not here to browse, are you?"},
            {"speaker": "PLAYER", "text": "..No."},
            {"speaker": "VISITOR", "text": "I saw you earlier."},
            {"speaker": "PLAYER", "text": "Doing what?"},
            {"speaker": "VISITOR", "text": "Watching everything."},
            {"speaker": "VISITOR", "text": "..Like her."},
            {"speaker": "PLAYER", "text": "You saw her too?"},
            {"speaker": "VISITOR", "text": "Yeah."},
            {"speaker": "VISITOR", "text": "She had this.. look."},
            {"speaker": "PLAYER", "text": "What kind of look?"},
            {"speaker": "VISITOR", "text": "Like she knew something no one else did."},
            {"speaker": "VISITOR", "text": "Like she was ahead of everyone."},
            {"speaker": "PLAYER", "text": "..Mischievous."},
            {"speaker": "VISITOR", "text": "Exactly."},
            {"speaker": "VISITOR", "text": "She wasn’t nervous."},
            {"speaker": "VISITOR", "text": "She was enjoying it."},
            {"speaker": "PLAYER", "text": "...a game."},
            {"speaker": "VISITOR", "text": "If you’re following her.."},
            {"speaker": "VISITOR", "text": "You’re close."},
        ],
    },

    # ===========================
    # 1990s NPC 8: Senior Curator
    # ===========================
    "senior_curator": {
        "dialogue": [
            {"speaker": "SENIOR CURATOR", "text": "This section is restricted."},
            {"speaker": "PLAYER", "text": "I need to be here."},
            {"speaker": "SENIOR CURATOR", "text": "..You remind me of him."},
            {"speaker": "PLAYER", "text": "My grandfather."},
            {"speaker": "SENIOR CURATOR", "text": "He built this place into what it is now."},
            {"speaker": "SENIOR CURATOR", "text": "A true museum of time."},
            {"speaker": "PLAYER", "text": "..I can see that."},
            {"speaker": "SENIOR CURATOR", "text": "He always believed.."},
            {"speaker": "SENIOR CURATOR", "text": "Time reveals everything eventually."},
            {"speaker": "PLAYER", "text": "A girl came through here."},
            {"speaker": "SENIOR CURATOR", "text": "Yes."},
            {"speaker": "PLAYER", "text": "What did she have?"},
            {"speaker": "SENIOR CURATOR", "text": "A necklace."},
            {"speaker": "SENIOR CURATOR", "text": "Long. Pearl."},
            {"speaker": "SENIOR CURATOR", "text": "Completely out of place."},
            {"speaker": "PLAYER", "text": "Where is it now?"},
            {"speaker": "SENIOR CURATOR", "text": "She hid it among archived accessories."},
            {"speaker": "SENIOR CURATOR", "text": "But it doesn’t belong."},
            {"speaker": "SENIOR CURATOR", "text": "You’ll recognize it immediately."},
        ],
    },
}

#testing

item_dialogue_data = {
    ("1920s", 10, 4): {
        "dialogue": [
            {"speaker": "PLAYER", "text": "Tall.. white.. doesn't belong.."},
            {"speaker": "PLAYER", "text": "There."},
            {"speaker": "PLAYER", "text": "..Go-Go boots."},
            {"speaker": "PLAYER", "text": "Definitely not from the 1920s."},
            {"speaker": "PLAYER", "text": "So the thief really is scattering items across time.."},
            {"speaker": "PLAYER", "text": "..and not even trying to hide the mismatch."},
            {"speaker": "DEVICE", "text": "Artifact recovered."},
            {"speaker": "DEVICE", "text": "Temporal jump requires stabilization."},
            {"speaker": "PLAYER", "text": "..Which means?"},
            {"speaker": "DEVICE", "text": "Mini-game required to calibrate timeline."},
            {"speaker": "PLAYER", "text": "..Of course there's a catch."},
            {"speaker": "PLAYER", "text": "Nothing can ever be simple."},
            {"speaker": "GAME", "text": "Mini-game starts somewhere here"}
        ],
        "quest": "boots_recovered"
    }
}