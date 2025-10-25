"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { ChevronDown, User, LogOut } from "lucide-react"

import { useIsMobile } from "@/hooks/use-mobile"
import { useAppStore } from "@/store/app-store"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
import { LoginModal } from "@/components/auth/LoginModal"

// ListItem helper for dropdown rows
function ListItem({
  title,
  children,
  href,
  ...props
}: React.ComponentPropsWithoutRef<"li"> & { href: string }) {
  return (
    <li {...props}>
      <NavigationMenuLink asChild>
        <Link 
          href={href} 
          className="block rounded-md p-2 hover:bg-[rgba(63,64,63,0.06)] transition"
        >
          <div className="text-sm leading-none font-norwester text-[#3f403f]">
            {title}
          </div>
          <p className="text-[13px] leading-snug text-[#575b44] line-clamp-2">
            {children}
          </p>
        </Link>
      </NavigationMenuLink>
    </li>
  )
}

export default function NavBar() {
  const pathname = usePathname()
  const isMobile = useIsMobile()
  const [showLoginModal, setShowLoginModal] = useState(false)
  const { user, signOut } = useAppStore()

  return (
    <nav className="sticky top-0 z-50 backdrop-blur supports-[backdrop-filter]:bg-[#fffbef]/70 border-b border-[rgba(63,64,63,0.08)]">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Brand */}
          <Link 
            href="/" 
            className="font-modular text-xl tracking-wide text-[#3f403f] hover:text-[#575b44] transition"
          >
            STUDY SPARK
          </Link>

          {/* Navigation Menu */}
          <NavigationMenu>
            <NavigationMenuList>
              {/* Home */}
              <NavigationMenuItem>
                <NavigationMenuLink asChild>
                  <Link 
                    href="/"
                    className={`${navigationMenuTriggerStyle()} font-norwester text-[#3f403f] hover:bg-[rgba(63,64,63,0.06)] rounded-xl px-4 py-2 ${
                      pathname === "/" ? "bg-[rgba(63,64,63,0.06)]" : ""
                    }`}
                  >
                    Home
                  </Link>
                </NavigationMenuLink>
              </NavigationMenuItem>

              {/* Study Methods */}
              <NavigationMenuItem>
                <NavigationMenuTrigger className={`group font-norwester text-[#3f403f] hover:bg-[rgba(63,64,63,0.06)] rounded-xl px-4 py-2 ${
                  pathname.startsWith("/methods") ? "bg-[rgba(63,64,63,0.06)]" : ""
                }`}>
                  Study Methods{" "}
                  <ChevronDown className="relative top-[1px] ml-1 h-3 w-3 transition duration-200 group-data-[state=open]:rotate-180" />
                </NavigationMenuTrigger>
                <NavigationMenuContent className="z-[60] mt-4">
                  <ul className="grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px]">
                    <ListItem href="/methods/pomodoro" title="Pomodoro">
                      25 min focus, 5 min break. Longer break every 4 rounds.
                    </ListItem>
                    <ListItem href="/methods/flowtime" title="Flowtime">
                      Work until energy dips, then rest. No fixed timer.
                    </ListItem>
                    <ListItem href="/methods/52-17" title="52 / 17">
                      52 min work, 17 min break.
                    </ListItem>
                    <ListItem href="/methods/deep-work-90-20" title="Deep Work (90 / 20)">
                      90 min deep focus, 20 min rest.
                    </ListItem>
                    <ListItem href="/methods/blurting-sprint" title="Blurting Sprint">
                      Short recall bursts, then review.
                    </ListItem>
                    <ListItem href="/methods/phone-free-sprint" title="Phone-Free Sprint">
                      Lock your phone away and sprint.
                    </ListItem>
                  </ul>
                </NavigationMenuContent>
              </NavigationMenuItem>

              {/* Resources */}
              <NavigationMenuItem>
                <NavigationMenuTrigger className={`group font-norwester text-[#3f403f] hover:bg-[rgba(63,64,63,0.06)] rounded-xl px-4 py-2 ${
                  pathname.startsWith("/faq") || pathname.startsWith("/guides") || pathname.startsWith("/blog")
                    ? "bg-[rgba(63,64,63,0.06)]"
                    : ""
                }`}>
                  Resources{" "}
                  <ChevronDown className="relative top-[1px] ml-1 h-3 w-3 transition duration-200 group-data-[state=open]:rotate-180" />
                </NavigationMenuTrigger>
                <NavigationMenuContent className="z-[60] mt-4">
                  <ul className="grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px]">
                    <ListItem href="/faq" title="FAQ">
                      Find answers to common questions.
                    </ListItem>
                    <ListItem href="/guides" title="Tips & Guides">
                      Improve your study habits with expert advice.
                    </ListItem>
                    <ListItem href="/blog" title="Blog">
                      Read our latest articles and updates.
                    </ListItem>
                  </ul>
                </NavigationMenuContent>
              </NavigationMenuItem>

              {/* About Us */}
              <NavigationMenuItem>
                <NavigationMenuTrigger className={`group font-norwester text-[#3f403f] hover:bg-[rgba(63,64,63,0.06)] rounded-xl px-4 py-2 ${
                  pathname.startsWith("/about") || pathname.startsWith("/#methods")
                    ? "bg-[rgba(63,64,63,0.06)]"
                    : ""
                }`}>
                  About Us{" "}
                  <ChevronDown className="relative top-[1px] ml-1 h-3 w-3 transition duration-200 group-data-[state=open]:rotate-180" />
                </NavigationMenuTrigger>
                <NavigationMenuContent className="z-[60] mt-4">
                  <ul className="grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px]">
                    <ListItem href="/about#mission" title="Our Mission">
                      Learn about our goals and what drives us.
                    </ListItem>
                    <ListItem href="/about#how-it-works" title="How It Works">
                      Discover the features that help you focus.
                    </ListItem>
                    <ListItem href="/#methods" title="Study Methods">
                      Explore different techniques to boost productivity.
                    </ListItem>
                  </ul>
                </NavigationMenuContent>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            {user ? (
              <NavigationMenu>
                <NavigationMenuList>
                  <NavigationMenuItem>
                    <NavigationMenuTrigger className="font-norwester text-[#3f403f] hover:bg-[rgba(63,64,63,0.06)] rounded-xl px-4 py-2">
                      <User className="h-4 w-4 mr-2" /> {user.name || "Profile"}
                    </NavigationMenuTrigger>
                    <NavigationMenuContent className="z-[60] mt-4">
                      <ul className="grid gap-3 p-4 w-[180px]">
                        <ListItem href="/progress" title="Progress">
                          Track your study journey.
                        </ListItem>
                        <li className="block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-[rgba(63,64,63,0.06)] focus:bg-[rgba(63,64,63,0.06)]">
                          <button onClick={signOut} className="flex items-center text-sm leading-none font-norwester text-[#3f403f] w-full">
                            <LogOut className="h-4 w-4 mr-2" /> Sign Out
                          </button>
                        </li>
                      </ul>
                    </NavigationMenuContent>
                  </NavigationMenuItem>
                </NavigationMenuList>
              </NavigationMenu>
            ) : (
              <button
                onClick={() => setShowLoginModal(true)}
                className="font-norwester text-[#3f403f] hover:bg-[rgba(63,64,63,0.06)] rounded-xl px-4 py-2 transition"
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Login Modal */}
      <LoginModal open={showLoginModal} onOpenChange={setShowLoginModal} />
    </nav>
  )
}
