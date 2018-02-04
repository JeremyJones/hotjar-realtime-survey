"""Class for defining/overriding behaviours used in the summary part
of the survey dashboard.
"""

# default interfaces
from .behaviours.countSurveys.default import (countSurveysBehaviour \
                                              as defaultCountSurveysB)
from .behaviours.averageAge.default import (averageAgeBehaviour \
                                            as defaultAverageAgeB)
from .behaviours.genderRatio.default import (genderRatioBehaviour \
                                             as defaultGenderRatioB)
from .behaviours.topAnswers.default import (topColoursBehaviour \
                                            as defaultTopColoursB)
from .behaviours.lastAnswered.default import (lastAnsweredBehaviour \
                                              as defaultLastAnsweredB)

class Summariser():
    def __init__(self,
                 countSurveysBehaviour=None,
                 averageAgeBehaviour=None,
                 genderRatioBehaviour=None,
                 topColoursBehaviour=None,
                 lastAnsweredBehaviour=None) -> None:

        self._countSurveysBehaviour = countSurveysBehaviour or \
                                      defaultCountSurveysB
        self.countSurveysBehaviour = self._countSurveysBehaviour()

        self._averageAgeBehaviour = averageAgeBehaviour or \
                                    defaultAverageAgeB
        self.averageAgeBehaviour = self._averageAgeBehaviour()

        self._genderRatioBehaviour = genderRatioBehaviour or \
                                     defaultGenderRatioB
        self.genderRatioBehaviour = self._genderRatioBehaviour()

        self._topColoursBehaviour = topColoursBehaviour or \
                                    defaultTopColoursB
        self.topColoursBehaviour = self._topColoursBehaviour()
        
        self._lastAnsweredBehaviour = lastAnsweredBehaviour or \
                                      defaultLastAnsweredB
        self.lastAnsweredBehaviour = self._lastAnsweredBehaviour()

    def countSurveys(self, session) -> int:
        return self.countSurveysBehaviour.getResult(session)

    def averageAge(self, session) -> float:
        return self.averageAgeBehaviour.getResult(session)

    def genderRatio(self, session) -> dict:
        return self.genderRatioBehaviour.getResult(session)

    def topColours(self, session) -> list:
        return self.topColoursBehaviour.getResult(session)

    def lastAnswered(self, session) -> int:
        return self.lastAnsweredBehaviour.getResult(session)
