
# lets us define a template in python that IntelliJ will validate without flagging an unused code error.
TEMPLATE = lambda *args: False

# need to import these so they are available for introspection
from . import activity_details, all_activities, calendar, health, similar_activities, fit_ff_parameters, \
    some_activities, fit_power_parameters, define_segment, month
