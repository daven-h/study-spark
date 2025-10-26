export interface Settings{
workMin: number; // duration of work sessions
shortBreak: number; // short break duration in minutes
longBreak: number; //extended break after cycles
cyclesToLong: number; // number of cycles before a long break
attentionThresholdSec: number; // how many seconds of being unfocused before alert triggers
yawMax: number; // maximum head rotation before considered unfocused
pitchMax: number; // maximum head tilt (vertically) before considered unfocused
adaptiveEnabled: boolean, //enable disable pomo
blockedSites: string[]; // sites considered unfocused (youtube,reddit, twitter)
}

export const DEFAULT_SETTINGS: Settings = {
    workMin: 25,
  shortBreak: 5,
  longBreak: 15,
  cyclesToLong: 4,
  attentionThresholdSec: 30,
  yawMax: 30,
  pitchMax: 30,
  adaptiveEnabled: false,
  blockedSites: [],
}
