"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { LogOut } from "lucide-react"

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
          className="block rounded-md border border-[rgba(63,64,63,0.15)] p-3 hover:bg-[rgba(63,64,63,0.06)] hover:border-[#939f5c] transition-all"
        >
          <div className="text-sm leading-none font-norwester text-[#3f403f] font-semibold">
            {title}
          </div>
          <p className="text-[13px] leading-snug text-[#575b44] line-clamp-2 mt-1">
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
  
  // Helper for avatar letter (handles null/undefined)
  const avatarLetter = (user?.email ?? '?')[0]?.toUpperCase() ?? '?';

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
                  Study Methods
                </NavigationMenuTrigger>
                <NavigationMenuContent className="z-[60] mt-8">
                  <ul className="grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px]">
                    <ListItem href="/methods/pomodoro" title="Pomodoro">
                      25 min focus, 5 min break. Longer break every 4 rounds.
                    </ListItem>
                    <ListItem href="/methods/52-17" title="52 / 17">
                      52 min work, 17 min break.
                    </ListItem>
                    <ListItem href="/methods/deep-work-90-20" title="Deep Work (90 / 20)">
                      90 min deep focus, 20 min rest.
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
                  Resources
                </NavigationMenuTrigger>
                <NavigationMenuContent className="z-[60] mt-8">
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
                <NavigationMenuLink asChild>
                  <Link 
                    href="/about"
                    className={`${navigationMenuTriggerStyle()} font-norwester text-[#3f403f] hover:bg-[rgba(63,64,63,0.06)] rounded-xl px-4 py-2 ${
                      pathname.startsWith("/about")
                        ? "bg-[rgba(63,64,63,0.06)]"
                        : ""
                    }`}
                  >
                    About Us
                  </Link>
                </NavigationMenuLink>
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
                      <div className="flex items-center">
                        <div className="w-6 h-6 bg-[#939f5c] rounded-full flex items-center justify-center mr-2">
                          <span className="text-xs font-modular text-[#3f403f]">{avatarLetter}</span>
                        </div>
                        <span className="text-sm">{user.email || user.name || "Profile"}</span>
                      </div>
                    </NavigationMenuTrigger>
                    <NavigationMenuContent className="z-[60] mt-8">
                      <ul className="grid gap-3 p-4 w-[180px]">
                        <ListItem href="/progress" title="Progress">
                          Track your study journey.
                        </ListItem>
                        <li className="block select-none space-y-1 rounded-md border border-[rgba(63,64,63,0.15)] p-3 leading-none no-underline outline-none transition-colors hover:bg-[rgba(63,64,63,0.06)] hover:border-[#939f5c] focus:bg-[rgba(63,64,63,0.06)]">
                          <button onClick={signOut} className="flex items-center text-sm leading-none font-norwester text-[#3f403f] w-full font-semibold">
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
