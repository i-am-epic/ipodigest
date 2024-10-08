"use client"; // This is a client component 👈🏽

import { useState, useEffect } from 'react'
import Link from 'next/link'
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

interface IPO {
    id: string
    company_name: string
    price: string
    gmp: string
    est_listing: string
    fire_rating: string
    ipo_size: string
    lot: string
    open_date: string
    close_date: string
    listing_date: string
}

// Function to determine row color based on status
const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
        case 'live':
            return 'bg-green-100 text-green-800'
        case 'closed':
            return 'bg-gray-100 text-gray-800'
        case 'upcoming':
            return 'bg-yellow-100 text-yellow-800'
        case 'waiting for listing':
            return 'bg-blue-100 text-blue-800'
        default:
            return ''
    }
}

// Function to format date string by appending the current year
const formatDate = (dateString: string) => {
    const currentYear = new Date().getFullYear()
    return new Date(`${dateString}-${currentYear}`)
}

// Function to calculate the status based on open_date, close_date, and listing_date
const getStatus = (openDate: string, closeDate: string, listingDate: string) => {
    const open = formatDate(openDate)
    const close = formatDate(closeDate)
    const listing = formatDate(listingDate)
    const today = new Date()

    if (today >= open && today <= close) {
        return 'live'
    } else if (today > close && today < listing) {
        return 'waiting for listing'
    } else if (today >= listing) {
        return 'closed'
    } else if (today < open) {
        return 'upcoming'
    }
    return ''
}

export default function IPOTable() {

    const [isMounted, setIsMounted] = useState(false)
    const [ipos, setIpos] = useState<IPO[]>([])

    // Set isMounted on first render to allow rendering
    useEffect(() => {
        setIsMounted(true)

        // Fetch IPO data when component is mounted
        const fetchIPOs = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/scrape-ipo', {
                    method: 'GET',
                    headers: {
                        accept: 'application/json',
                    },
                })
                const data = await response.json()
                setIpos(data)
            } catch (error) {
                console.error("Error fetching IPO data:", error)
            }
        }

        fetchIPOs()
    }, [])

    if (!isMounted) {
        return null // Prevent rendering on server-side
    }

    return (
        <Table>
            <TableCaption>List of current IPOs available for investment.</TableCaption>
            <TableHeader>
                <TableRow>
                    <TableHead>Company Name</TableHead>
                    <TableHead>Price</TableHead>
                    <TableHead>Open Date</TableHead>
                    <TableHead>Close Date</TableHead>
                    <TableHead>Listing Date</TableHead>
                    <TableHead>Status</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {ipos.map((ipo, index) => {
                    const status = getStatus(ipo.open_date, ipo.close_date, ipo.listing_date)
                    return (
                        <TableRow key={index} className={getStatusColor(status)}>
                            <TableCell>
                                <Link href={`/ipo/${ipo.id}`} className="text-blue-500 hover:underline">
                                    {ipo.company_name}
                                </Link>
                            </TableCell>
                            <TableCell>{ipo.price}</TableCell>
                            <TableCell>{ipo.open_date}</TableCell>
                            <TableCell>{ipo.close_date}</TableCell>
                            <TableCell>{ipo.listing_date}</TableCell>
                            <TableCell>{status}</TableCell>
                        </TableRow>
                    )
                })}
            </TableBody>
        </Table>
    )
}
