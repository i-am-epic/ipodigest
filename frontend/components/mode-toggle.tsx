"use client"

import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

import { Button } from "./ui/button"

export function ModeToggle() {
    const { theme, setTheme } = useTheme()

    // Function to toggle between light and dark mode
    const toggleTheme = () => {
        const newTheme = theme === "dark" ? "light" : "dark"
        setTheme(newTheme)
        localStorage.setItem("theme", newTheme) // Persisting theme in localStorage
    }

    // Load theme from localStorage on initial render
    React.useEffect(() => {
        const savedTheme = localStorage.getItem("theme")
        if (savedTheme) {
            setTheme(savedTheme)
        }
    }, [setTheme])

    return (
        <Button variant="outline" size="icon" onClick={toggleTheme}>
            {theme === "dark" ? (
                <Sun className="h-[1.2rem] w-[1.2rem]" />
            ) : (
                <Moon className="h-[1.2rem] w-[1.2rem]" />
            )}
            <span className="sr-only">Toggle theme</span>
        </Button>
    )
}
