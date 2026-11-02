#!/usr/bin/env python3
"""
The four calibration inputs from Milestone 4, plus the plain-writer control
that detector.py says to add.

    python calibrate.py

Prints every measure, both signals and the label, so the anchors in
stylometry.py can be set against something rather than guessed.
"""

import detector
import scoring
import stylometry

PLAIN_HUMAN = (
    "F1 is a bit of a weird as a sport in terms of length of time a race "
    "takes. Typically non F1 fans in the past would make remarks to me like "
    "they go on forever but now with the DtS generation I often find myself "
    "explaining in very brief terms that we can guess that Monza will be over "
    "very quickly if it's dry and why that is. I doubt the vast majority of "
    "F1's newer fans will notice any difference with these lap reductions. If "
    "I ever get frustrated explaining conditions, duration and quirks I remind "
    "myself that F1 is probably still easier than cricket."
)

HUMAN = (
    "As the younger generations are brought up on everything happening more "
    "quickly or instantly, and people start to accept sprint races are not "
    "going (begrudgingly), I am sure there will start to be questions raised "
    "about making race distances shorter. I am, to be honest pleasantly "
    "surprised that F1 have said that the full race distances will be restored "
    "in 2028. I was not expecting that. As with everything it depends on the "
    "quality of the 'entertainment'. A boring standard full length race can "
    "seem interminable if there's not much going on or no real battles for "
    "places."
)

AI = (
    "The implementation of a shorter race format requires careful "
    "consideration of several important factors. First, it is important to "
    "note that race length has a significant impact on the overall viewer "
    "experience. Additionally, teams must adapt their strategies to account "
    "for a reduced number of laps. Furthermore, the reduction in distance may "
    "affect tyre management, which has traditionally been a key component of "
    "race strategy. Overall, while there are benefits to a shorter format, it "
    "is essential that the governing body carefully weighs these against the "
    "potential drawbacks before implementing any permanent changes to the "
    "existing structure."
)

LIGHTLY_EDITED_AI = (
    "The implemntation of a shorter race format requires careful "
    "consideration of several important factors. First, race length has a "
    "signficant impact on the viewer experience. It just does. Additionally, "
    "teams must adapt their strategies to account for a reduced number of "
    "laps, and the reduction in distance may affect tyre managment, which has "
    "traditionally been a key component of race strategy — something the "
    "governing body keeps forgetting. Overall, while there are benefits to a "
    "shorter format, it is essential that these are weighed against the "
    "drawbacks before any permanent changes are made. Anyway. That's my take."
)

INPUTS = [
    ("clearly AI", AI),
    ("clearly human", HUMAN),
    ("plain conventional human", PLAIN_HUMAN),
    ("lightly-edited AI", LIGHTLY_EDITED_AI),
]


def main():
    for name, text in INPUTS:
        model = detector.model_signal(text)
        style = stylometry.style_signal(text)
        combined = scoring.combine_signals(model, style)
        guess, _ = scoring.score_to_label(combined)

        print(f"\n{name}")
        print(f"  perplexity    {detector.perplexity(text):7.1f}")
        print(f"  spread        {stylometry.sentence_length_spread(text):7.3f}")
        print(f"  variety       {stylometry.type_token_ratio(text):7.3f}")
        print(f"  punctuation   {stylometry.punctuation_density(text):7.3f}")
        print(f"  model_score   {model:7.4f}")
        print(f"  style_score   {style:7.4f}")
        print(f"  combined      {combined:7.4f}   -> {guess}")


if __name__ == "__main__":
    main()
