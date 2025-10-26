'use client';

import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { useAppStore } from '@/store/app-store';

interface DailyGoalSheetProps {
  currentGoal: number; // in minutes
}

export function DailyGoalSheet({ currentGoal }: DailyGoalSheetProps) {
  const { setDailyGoal } = useAppStore();
  const [goalMinutes, setGoalMinutes] = useState(currentGoal);
  const [isOpen, setIsOpen] = useState(false);

  const handleSave = () => {
    if (goalMinutes > 0 && goalMinutes <= 1440) { // Max 24 hours
      setDailyGoal(goalMinutes);
      setIsOpen(false);
    }
  };

  const formatGoal = (minutes: number) => {
    if (minutes < 60) {
      return `${minutes} minutes`;
    } else if (minutes === 60) {
      return '1 hour';
    } else if (minutes % 60 === 0) {
      return `${minutes / 60} hours`;
    } else {
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = minutes % 60;
      return `${hours}h ${remainingMinutes}m`;
    }
  };

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button 
          variant="outline" 
          className="font-norwester text-[#3f403f] border-[rgba(63,64,63,0.08)] hover:bg-[rgba(63,64,63,0.06)]"
        >
          Set Goal
        </Button>
      </SheetTrigger>
      <SheetContent className="bg-[#fffbef] border-l border-[rgba(63,64,63,0.08)]">
        <SheetHeader>
          <SheetTitle className="font-modular text-[#3f403f]">
            Set Daily Study Goal
          </SheetTitle>
          <SheetDescription className="font-norwester text-[#575b44]">
            Choose how many minutes you want to study each day. This will help you track your progress and stay motivated.
          </SheetDescription>
        </SheetHeader>
        
        <div className="grid flex-1 auto-rows-min gap-6 px-4 py-6">
          <div className="grid gap-3">
            <Label 
              htmlFor="daily-goal-minutes" 
              className="font-norwester text-[#3f403f]"
            >
              Daily Goal (minutes)
            </Label>
            <Input 
              id="daily-goal-minutes" 
              type="number"
              min="1"
              max="1440"
              value={goalMinutes}
              onChange={(e) => setGoalMinutes(parseInt(e.target.value) || 0)}
              className="font-norwester text-[#3f403f] border-[rgba(63,64,63,0.08)] focus:border-[#939f5c]"
              placeholder="Enter minutes (e.g., 120 for 2 hours)"
            />
            <p className="text-sm font-norwester text-[#575b44]">
              Current goal: <span className="font-modular text-[#939f5c]">{formatGoal(currentGoal)}</span>
            </p>
            <p className="text-sm font-norwester text-[#575b44]">
              New goal: <span className="font-modular text-[#939f5c]">{formatGoal(goalMinutes)}</span>
            </p>
          </div>
          
          {/* Quick preset buttons */}
          <div className="grid gap-3">
            <Label className="font-norwester text-[#3f403f]">
              Quick Presets
            </Label>
            <div className="grid grid-cols-2 gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setGoalMinutes(30)}
                className="font-norwester text-[#3f403f] border-[rgba(63,64,63,0.08)] hover:bg-[rgba(63,64,63,0.06)]"
              >
                30 min
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setGoalMinutes(60)}
                className="font-norwester text-[#3f403f] border-[rgba(63,64,63,0.08)] hover:bg-[rgba(63,64,63,0.06)]"
              >
                1 hour
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setGoalMinutes(90)}
                className="font-norwester text-[#3f403f] border-[rgba(63,64,63,0.08)] hover:bg-[rgba(63,64,63,0.06)]"
              >
                1.5 hours
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setGoalMinutes(120)}
                className="font-norwester text-[#3f403f] border-[rgba(63,64,63,0.08)] hover:bg-[rgba(63,64,63,0.06)]"
              >
                2 hours
              </Button>
            </div>
          </div>
        </div>
        
        <SheetFooter className="gap-2">
          <Button 
            type="button"
            onClick={handleSave}
            disabled={goalMinutes <= 0 || goalMinutes > 1440}
            className="font-modular bg-[#939f5c] text-[#3f403f] hover:bg-[#808b4f] border-0"
          >
            Save Goal
          </Button>
          <SheetClose asChild>
            <Button 
              variant="outline"
              className="font-norwester text-[#3f403f] border-[rgba(63,64,63,0.08)] hover:bg-[rgba(63,64,63,0.06)]"
            >
              Cancel
            </Button>
          </SheetClose>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
