"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Sheet, SheetClose, SheetContent, SheetDescription, SheetFooter, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { useAppStore } from "@/store/app-store";
import type { MethodSlug } from "@/types";

export default function AddSessionSheet({ className }: { className?: string }) {
  const addSession = useAppStore(s => s.addSession);
  const [title, setTitle] = useState("");
  const [method, setMethod] = useState<MethodSlug>("pomodoro");
  const [completed, setCompleted] = useState(true);
  const [minutes, setMinutes] = useState<number>(25);
  const [dateISO, setDateISO] = useState<string>(new Date().toISOString().slice(0,10));

  function onSave() {
    if (!title.trim()) return;
    if (completed && (!minutes || minutes <= 0)) return;
    
    const newSession = {
      id: `session-${Date.now()}`,
      title: title.trim(),
      method,
      completed,
      minutes: completed ? minutes : 0,
      dateISO,
      createdAt: Date.now()
    };
    
    addSession(newSession);
    
    // Reset form
    setTitle("");
    setMethod("pomodoro");
    setCompleted(true);
    setMinutes(25);
    setDateISO(new Date().toISOString().slice(0,10));
  }

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button className="font-modular rounded-2xl bg-[#939f5c] text-[#3f403f] hover:bg-[#808b4f]">
          Add Task / Session
        </Button>
      </SheetTrigger>
      <SheetContent className="sm:max-w-[520px]">
        <SheetHeader>
          <SheetTitle className="font-modular text-[#3f403f]">Add Task / Session</SheetTitle>
          <SheetDescription className="font-norwester text-[#575b44]">
            Log what you studied so your insights stay up to date.
          </SheetDescription>
        </SheetHeader>

        <div className="mt-6 grid gap-5 md:grid-cols-2">
          <div className="grid gap-2 md:col-span-2">
            <Label htmlFor="title" className="font-norwester text-[#575b44]">Title</Label>
            <Input 
              id="title" 
              value={title} 
              onChange={e => setTitle(e.target.value)} 
              placeholder="e.g., Biology Chapter 5" 
            />
          </div>

          <div className="grid gap-2">
            <Label className="font-norwester text-[#575b44]">Study Method</Label>
            <Select value={method} onValueChange={(v) => setMethod(v as MethodSlug)}>
              <SelectTrigger>
                <SelectValue placeholder="Choose a method" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="pomodoro">Pomodoro</SelectItem>
                <SelectItem value="52-17">52 / 17</SelectItem>
                <SelectItem value="deep-work-90-20">Deep Work (90 / 20)</SelectItem>
                <SelectItem value="phone-free-sprint">Phone-Free Sprint</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="minutes" className="font-norwester text-[#575b44]">Focus Minutes</Label>
            <Input 
              id="minutes" 
              type="number" 
              min={0} 
              value={minutes} 
              onChange={e => setMinutes(Number(e.target.value))} 
              disabled={!completed} 
            />
          </div>

          <div className="grid gap-2">
            <Label htmlFor="date" className="font-norwester text-[#575b44]">Date</Label>
            <Input 
              id="date" 
              type="date" 
              value={dateISO} 
              onChange={e => setDateISO(e.target.value)} 
            />
          </div>

          <div className="flex items-center gap-2 md:col-span-2">
            <Checkbox 
              id="completed" 
              checked={completed} 
              onCheckedChange={(v) => setCompleted(Boolean(v))} 
            />
            <Label htmlFor="completed" className="font-norwester text-[#575b44]">Completed</Label>
          </div>
        </div>

        <SheetFooter className="mt-6">
          <Button
            type="button"
            onClick={onSave}
            className="font-modular rounded-2xl bg-[#939f5c] text-[#3f403f] hover:bg-[#808b4f]"
          >
            Save
          </Button>
          <SheetClose asChild>
            <Button variant="outline">Close</Button>
          </SheetClose>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
