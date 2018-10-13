
from .default import default
from ..config.database import Counter, add_topic, add_child_topic, add_topic_field
from ..uweird.fields import Text


def acooke(db):

    default(db)

    with db.session_context() as s:

        c = Counter(100)

        injuries = add_topic(s, 'Inuries', c)

        ms = add_child_topic(s, injuries, 'Multiple Sclerosis', c)
        add_topic_field(s, ms, 'Notes', c,
                        display_cls=Text)
        add_child_topic(s, ms, 'Betaferon', c,
                        schedule='2018-08-07/2d')  # reminder to take meds on alternate days

        leg = add_child_topic(s, injuries, 'Broken Femur LHS', c,
                              schedule='2018-03-11-')
        add_topic_field(s, leg, 'Notes', c,
                        display_cls=Text)
        add_child_topic(s, leg, 'Learn to manage tendon pain', c)  # aims added as child topics
        add_child_topic(s, leg, 'Maintain fitness', c)
        add_child_topic(s, leg, 'Visit UK', c,
                        schedule='-2018-08-11')