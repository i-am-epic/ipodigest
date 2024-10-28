"use client"; // This is a client component 👈🏽

import { useState, useEffect } from 'react';
import Link from 'next/link';
import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@/components/ui/tabs";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

interface IPO {
    ipo_id: string;
    company_name: string;
    price: string;
    status: string;
    issue_size: number;
    lot_size: number;
    open_date: string;
    close_date: string;
    listing_date: string;
    listing_at: string;
}

// Function to format the status based on the new JSON response
const getStatus = (status: string) => {
    switch (status.toLowerCase()) {
        case 'current':
            return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
        case 'past':
            return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
        case 'upcoming':
            return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
        case 'waiting for listing':
            return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
        default:
            return '';
    }
};

export default function IPOTabs() {
    const [isMounted, setIsMounted] = useState(false);
    const [ipos, setIpos] = useState<IPO[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setIsMounted(true);

        const fetchIPOs = async () => {
            try {
                setIsLoading(true);
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/ipo/list?page=1&limit=10`, {
                    method: 'GET',
                    headers: { accept: 'application/json' },
                });
                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }
                const data = await response.json();

                // Map data to match the IPO interface
                const formattedIpos = data.data.ipos.map((ipo: any) => ({
                    ipo_id: ipo.ipo_id,
                    company_name: ipo.company_name,
                    price: ipo.price_band.min && ipo.price_band.max
                        ? `${ipo.price_band.min}-${ipo.price_band.max}`
                        : "N/A",
                    status: ipo.status,
                    issue_size: ipo.issue_size,
                    lot_size: ipo.lot_size,
                    open_date: ipo.subscription_dates.opens,
                    close_date: ipo.subscription_dates.closes,
                    listing_date: ipo.listing_date,
                    listing_at: ipo.listing_at
                }));
                setIpos(formattedIpos);
            } catch (error) {
                console.error("Error fetching IPO data:", error);
                setError("Failed to load IPO data. Please try again later.");
            } finally {
                setIsLoading(false);
            }
        };

        fetchIPOs();
    }, []);

    if (!isMounted) return null; // Prevent rendering on server-side

    return (
        <Tabs defaultValue="all" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="current">Current</TabsTrigger>
                <TabsTrigger value="past">Past</TabsTrigger>
            </TabsList>

            <TabsContent value="all">
                {(() => {
                    if (isLoading) return <Loading />;
                    if (error) return <Error message={error} />;
                    return <IPOTable ipos={ipos} />;
                })()}
            </TabsContent>

            <TabsContent value="current">
                {isLoading ? <Loading /> : <IPOTable ipos={ipos.filter(ipo => ipo.status === 'current')} />}
            </TabsContent>

            <TabsContent value="past">
                {isLoading ? <Loading /> : <IPOTable ipos={ipos.filter(ipo => ipo.status === 'past')} />}
            </TabsContent>
        </Tabs>
    );
}

// IPO Table Component
function IPOTable({ ipos }: { ipos: IPO[] }) {
    return (
        <Table className="w-full text-sm">
            <TableCaption>List of IPOs based on the selected category.</TableCaption>
            <TableHeader>
                <TableRow>
                    <TableHead>Company Name</TableHead>
                    <TableHead>Price Band</TableHead>
                    <TableHead>Open Date</TableHead>
                    <TableHead>Close Date</TableHead>
                    <TableHead>Listing Date</TableHead>
                    <TableHead>Listing At</TableHead>
                    <TableHead>Status</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {ipos.map((ipo) => (
                    <TableRow key={ipo.ipo_id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                        <TableCell>
                            <Link href={`/ipo/${ipo.ipo_id}`} className="text-blue-500 hover:underline">
                                {ipo.company_name}
                            </Link>
                        </TableCell>
                        <TableCell>{ipo.price}</TableCell>
                        <TableCell>{ipo.open_date}</TableCell>
                        <TableCell>{ipo.close_date}</TableCell>
                        <TableCell>{ipo.listing_date}</TableCell>
                        <TableCell>{ipo.listing_at}</TableCell>
                        <TableCell className={`p-2 rounded ${getStatus(ipo.status)}`}>
                            {ipo.status}
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    );
}

// Loading Spinner Component
function Loading() {
    return (
        <div className="flex justify-center items-center p-8">
            <div className="loader"></div> {/* Replace with a spinner UI */}
            <p className="ml-4">Loading...</p>
        </div>
    );
}

// Error Message Component
function Error({ message }: { message: string }) {
    return (
        <div className="text-red-500 text-center p-4">
            {message}
        </div>
    );
}
