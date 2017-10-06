#!/usr/bin/env python3.5
import logging

logging.basicConfig(filename='states.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class StateHandler:
  def __init__(self, initialState, states, fallback, gamedata=None):
    self.logger = logging.getLogger(__name__)
    self.logger.info("Starting State Machine")
    self.logger.info("Entry Point: " + initialState.__class__.__name__)
    self.state = initialState
    self.all_states = states
    self.fallback = fallback
    self.gamedata = gamedata

  def run(self, *args):
    while True:
      if self.state in self.all_states:
        res, gamedata = self.state.run(self.gamedata)
        if gamedata != None:
          self.gamedata = gamedata
        self.logger.info("Next state: {0}".format(self.state.next(res).__class__.__name__))
        self.state = self.state.next(res)
      elif self.fallback != None:
        self.fallback.run(self.gamedata)
        return self.gamedata
      else:
        return self.gamedata 
