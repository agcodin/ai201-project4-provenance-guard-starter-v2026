"""
What your test runs. ← UNIT 8, MILESTONE 3

Five scenarios, one per criterion. `run_eval.py` runs everything here three
times, which is what the three-trial rule in criteria.md needs.

Scenario 1 is ten paragraphs of my own coursework, taken from two CGT 105
analysis essays in my Drive. It had to be my own writing rather than text from
anywhere else, because otherwise criterion 1 measures somebody else's prose and
reports it as my false-positive rate.

The human samples in scenarios 2 and 3 are real forum comments from the
RaceFans comment sections, collected for project 3. They are genuinely
human-written, which is what those two criteria need, and they are not mine,
which is why they are not in scenario 1.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Ten paragraphs from two pieces of my own coursework, pulled from my
        # Drive. Six are from a CGT 105 analysis of the controversy around
        # Grand Theft Auto V, four from a CGT 105 analysis of Computer Space.
        "texts": [
            'Grand Theft Auto V sparked debate from the day it released. People argued about its violence, its open criminal world, and the behavior it allowed the player to carry out. Many believed the game encouraged harmful acts because it allowed players to break the law without strict limits. The game became even more controversial as it reached a vast audience, extending its impact far beyond a niche group.',
            'Much of the debate around the game centered on its blend of realism and freedom. The game encourages free exploration, including stealing cars, fighting police, and interacting with civilians, often in chaotic ways. Critics raised concerns that the game rewards crime by making it easy and sometimes humorous. They said this tone made people worry the game would normalize behavior that would be harmful in real life.',
            "A key mechanic that shaped the game's reputation is the wanted level system. This mechanic determines how the police react when the player commits a crime. The game uses a star scale that climbs as the player does more damage or keeps resisting arrest. The system is transparent, predictable, and visible on screen. Each level increases police strength and adds new units.",
            'People criticized this system because they believed the chase became entertainment rather than a consequence. The player may begin crimes just to trigger these battles, and the game rewards escape with a sense of victory. The mechanic does not permanently punish crime. It resets after an escape, so the player can repeat the loop as often as they want.',
            'The game also faced complaints about how it treats certain groups. Some organizations said the game portrayed women in negative ways. Others said it encouraged players to commit violent acts with no moral reflection. They pointed to missions that involve torture, robberies, and aggressive fights. They argued that the game goes beyond simple fantasy and enters territory that feels uncomfortable due to its realistic graphics and animations.',
            'The controversy often comes from the gap between how the game behaves and how people think players interpret it. People who do not play may see only the worst parts of the game shown online. They see crime clips without seeing the whole system of consequences. They may also not understand that players use the world as a playground rather than a lesson.',
            'Released in 1971 by Nolan Bushnell and Ted Dabney, Computer Space was the first commercially sold arcade video game. The player controlled a rocket ship locked in combat with two flying saucers on a black starfield background. It was a bold attempt to merge futuristic themes with interactive electronics at a time when most people had never seen a video game before.',
            "The rules of Computer Space were straightforward but challenging to master. The player's goal was to destroy as many enemy saucers as possible before the timer expired. Two saucers moved randomly across the screen, firing slow-moving missiles at the player's ship. Each time a saucer was hit, the player earned a point.",
            "A typical minute of Computer Space begins with the player's rocket ship in the center of the screen. The saucers immediately begin moving across the starfield, firing at random intervals. The player rotates the ship toward one saucer, fires, and hits the thrust button to move closer. The ship glides across the screen, overshooting slightly due to inertia.",
            "The Computer Space cabinet was built from molded fiberglass painted in bright metallic colors such as red, blue, or green. The curved design looked futuristic, resembling a prop from a science fiction movie. A standard CRT monitor displayed the gameplay, while four control buttons were mounted on the front panel. Because the system ran entirely on logic circuits, every aspect of the game's behavior came from physical hardware rather than software.",
        ],
    },
    {
        "name": "score spread, clearly AI against clearly human",
        "criterion": 2,
        "texts": [
            'The introduction of a revised cost cap represents a significant development for the sport. It is important to note that financial regulations serve several key purposes, including the promotion of competitive balance and the long-term sustainability of participating organisations. Furthermore, teams must carefully allocate their resources in order to maximise performance within the established constraints. Overall, while the policy has been subject to criticism, it is widely regarded as a positive step forward.',
            'There are a number of important factors to consider when evaluating tyre strategy. First, track temperature has a considerable influence on degradation rates across a race distance. Additionally, the selection of compound must be balanced against the anticipated number of pit stops. Moreover, teams frequently adjust their approach in response to changing conditions. In conclusion, effective tyre management remains an essential component of overall race performance.',
            "Driver development programmes play a crucial role in the modern motorsport landscape. These initiatives are designed to identify promising talent at an early stage and provide structured support throughout a driver's career. It should be noted that such programmes require substantial investment from the organisations involved. Nevertheless, the benefits are considerable, as a well-prepared driver contributes significantly to the overall success of the team.",
            "The question of race calendar expansion has generated considerable discussion among stakeholders. On the one hand, additional events increase commercial revenue and broaden the sport's global reach. On the other hand, a longer season places additional demands on personnel and logistics. It is therefore essential that the governing body carefully weighs these competing priorities before finalising any future schedule.",
            'Aerodynamic regulations have undergone a series of important revisions in recent years. The primary objective of these changes is to reduce the turbulent air generated by the leading car, thereby improving the opportunity for overtaking. Additionally, the regulations aim to limit development costs through standardised components. Overall, the impact of these measures continues to be assessed by teams and observers alike.',
            'I was there. Great event, these cars are awesome and they sound glorious which is not something you say as often in Motorsport these days. Hopefully next time, if they ever come back and I hope they will, they announce it better because it wasn’t sold out although the weather warning we had before the weekend didn’t help, surely',
            'The amount of overspend that the FIA identified was the same amount as another team’s entire development budget. That would easily explain enough of the success to contaminate the results. (You probably don’t want to get into the discussion of whether it was the sole reason, given I’m one of the people who identified at least 3 other FIA regulation breaches that helped Red Bull in 2021…)',
            'I disagree, I’m thinking the same as asz: 2 mil is a very minor overspend, you can’t really call that the difference between having a dominant team or simply a top team, back in the days ferrari would spend tens of millions more than other teams, yet apart from the schumacher era they weren’t very dominant over the f1 history, and even during that era there’s only 3 dominant seasons at best, some don’t even call 2001 dominant, after all hakkinen wasn’t performing at his usual level for a comparison.',
            'Wouldn’t change my view. And Aston Martin are a classic example of it not just being about the money. The series was on its knees financially and albeit it wasn’t just because of the cap, having limited resources means you need to be smarter rather just pouring money into an arms race that gave us one team domination to no one’s benefit bar the team itself',
            'What a silly man, if there is no cap, of course you will have opportunities to improve your car but the big teams will spend even more than you so you’re upgrades will be good for nothing. If anything it is the tight design regulations that prevent new radical ideas or them changing every so often resets the the team catching up.',
        ],
    },
    {
        "name": "label coverage across the score range",
        "criterion": 3,
        "texts": [
            # One expected in each band: AI, borderline, human.
            'The introduction of a revised cost cap represents a significant development for the sport. It is important to note that financial regulations serve several key purposes, including the promotion of competitive balance and the long-term sustainability of participating organisations. Furthermore, teams must carefully allocate their resources in order to maximise performance within the established constraints. Overall, while the policy has been subject to criticism, it is widely regarded as a positive step forward.',
            'I think the cap is fine in principle but the enforcement is the part nobody wants to talk about. If the penalty for going over is a fine and a bit of wind tunnel time then the maths works out in favour of spending anyway, which is roughly what happened the first time it was tested. Either the sanction has to hurt more than the advantage does or the whole thing is just paperwork that the bigger teams are better resourced to handle.',
            'I was there. Great event, these cars are awesome and they sound glorious which is not something you say as often in Motorsport these days. Hopefully next time, if they ever come back and I hope they will, they announce it better because it wasn’t sold out although the weather warning we had before the weekend didn’t help, surely',
        ],
    },
    {
        # Criterion 4 cannot be expressed as text alone, because an appeal needs
        # a content_id that came back from a submission first. These submissions
        # exist to produce ids, and the appeals themselves are run by hand with
        # curl, which is what the write-up says.
        "name": "appeal path, submissions that produce ids to appeal against",
        "criterion": 4,
        "texts": [
            'There are a number of important factors to consider when evaluating tyre strategy. First, track temperature has a considerable influence on degradation rates across a race distance. Additionally, the selection of compound must be balanced against the anticipated number of pit stops. Moreover, teams frequently adjust their approach in response to changing conditions. In conclusion, effective tyre management remains an essential component of overall race performance.',
            'The amount of overspend that the FIA identified was the same amount as another team’s entire development budget. That would easily explain enough of the success to contaminate the results. (You probably don’t want to get into the discussion of whether it was the sole reason, given I’m one of the people who identified at least 3 other FIA regulation breaches that helped Red Bull in 2021…)',
            'I think the cap is fine in principle but the enforcement is the part nobody wants to talk about. If the penalty for going over is a fine and a bit of wind tunnel time then the maths works out in favour of spending anyway, which is roughly what happened the first time it was tested. Either the sanction has to hurt more than the advantage does or the whole thing is just paperwork that the bigger teams are better resourced to handle.',
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
