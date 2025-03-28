"use client";

import { useState, useEffect, useMemo } from "react";
import { debounce } from "lodash";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import {
  X,
  Search,
  ChevronRight,
  GitCompare,
  BarChart2,
  Star,
  TrendingUp,
  Zap,
  List,
  PieChart,
} from "lucide-react";
import Link from "next/link";

interface App {
  id: string;
  apple_id: string;
  name: string;
  developer: string;
  category: string;
  list_type: string;
  price: string;
  rank: number;
  monthly_revenue_estimate: number;
  monthly_downloads_estimate: number;
  icon_url: string;
  subtitle: string;
}

export function CompareSection() {
  const [searchQuery1, setSearchQuery1] = useState("");
  const [searchQuery2, setSearchQuery2] = useState("");
  const [searchResults1, setSearchResults1] = useState<App[]>([]);
  const [searchResults2, setSearchResults2] = useState<App[]>([]);
  const [selectedApp1, setSelectedApp1] = useState<App | null>(null);
  const [selectedApp2, setSelectedApp2] = useState<App | null>(null);
  const [isSearching1, setIsSearching1] = useState(false);
  const [isSearching2, setIsSearching2] = useState(false);

  const formatCompactNumber = (num: number): string => {
    if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`;
    if (num >= 1_000) return `${(num / 1_000).toFixed(0)}K`;
    return num.toString();
  };

  const searchApps = async (
    query: string,
    setResults: (apps: App[]) => void,
    setIsSearching: (val: boolean) => void
  ) => {
    if (!query.trim()) {
      setResults([]);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    try {
      const url = new URL(`${process.env.NEXT_PUBLIC_API_URL}/apps/search`);
      url.searchParams.set("q", query);
      url.searchParams.set("limit", "5");

      const res = await fetch(url.toString());
      const data = await res.json();
      setResults(data?.apps || []);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setIsSearching(false);
    }
  };

  const debouncedSearch1 = useMemo(
    () =>
      debounce((query: string) => {
        searchApps(query, setSearchResults1, setIsSearching1);
      }, 300),
    []
  );

  const debouncedSearch2 = useMemo(
    () =>
      debounce((query: string) => {
        searchApps(query, setSearchResults2, setIsSearching2);
      }, 300),
    []
  );

  useEffect(() => {
    if (searchQuery1) {
      debouncedSearch1(searchQuery1);
    } else {
      setSearchResults1([]);
      setIsSearching1(false);
    }

    return () => debouncedSearch1.cancel();
  }, [searchQuery1, debouncedSearch1]);

  useEffect(() => {
    if (searchQuery2) {
      debouncedSearch2(searchQuery2);
    } else {
      setSearchResults2([]);
      setIsSearching2(false);
    }

    return () => debouncedSearch2.cancel();
  }, [searchQuery2, debouncedSearch2]);

  const selectApp = (
    app: App,
    setSelectedApp: (app: App) => void,
    setSearchResults: (apps: App[]) => void
  ) => {
    setSelectedApp(app);
    setSearchResults([]);
  };

  const clearSelection = (
    setSelectedApp: (app: null) => void,
    setSearchQuery: (query: string) => void
  ) => {
    setSelectedApp(null);
    setSearchQuery("");
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto px-4 py-6">
      {/* PARTE DE CIMA DA SECTION */}
      <div className="text-center space-y-6">
        <h2 className="text-4xl font-bold tracking-tight">
          Compare Apps Side by Side
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Compare key metrics between two apps to make informed decisions
        </p>
      </div>

      {/* CARDS COM AS INFOS */}
      {!selectedApp1 && !selectedApp2 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="hover:-translate-y-1 transition-transform duration-200">
            <CardContent className="p-6 flex items-center gap-4">
              <div className="bg-primary/10 text-primary p-3 rounded-full">
                <Zap className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold">Quick Comparison</h3>
                <p className="text-sm text-muted-foreground">
                  Enter two app names to get started
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:-translate-y-1 transition-transform duration-200">
            <CardContent className="p-6 flex items-center gap-4">
              <div className="bg-primary/10 text-primary p-3 rounded-full">
                <List className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold">Top Categories</h3>
                <p className="text-sm text-muted-foreground">
                  Games, Business, Education, Health, Entertainment
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:-translate-y-1 transition-transform duration-200">
            <CardContent className="p-6 flex items-center gap-4">
              <div className="bg-primary/10 text-primary p-3 rounded-full">
                <PieChart className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold">Key Metrics</h3>
                <p className="text-sm text-muted-foreground">
                  Downloads, Revenue, Ratings, Rankings
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* AS BOX PARA ESCREVER O NOME DO APP */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* APP 1 */}
        <Card className="hover:shadow-md transition-shadow">
          <CardContent className="p-4">
            {selectedApp1 ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center gap-4">
                  <Link
                    href={`/apps/${selectedApp1.apple_id}`}
                    className="flex items-center gap-4 group flex-1"
                  >
                    <img
                      src={selectedApp1.icon_url}
                      alt={selectedApp1.name}
                      className="w-14 h-14 rounded-xl object-cover border"
                    />
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold truncate group-hover:text-primary transition-colors">
                        {selectedApp1.name}
                      </h3>
                      <p className="text-sm text-muted-foreground truncate">
                        {selectedApp1.developer}
                      </p>
                      <div className="flex gap-1 mt-1">
                        <span className="text-xs bg-accent px-2 py-0.5 rounded">
                          {selectedApp1.category}
                        </span>
                        {selectedApp1.rank && (
                          <span className="text-xs bg-accent px-2 py-0.5 rounded">
                            #{selectedApp1.rank}
                          </span>
                        )}
                      </div>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:text-primary" />
                  </Link>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="shrink-0"
                    onClick={() =>
                      clearSelection(setSelectedApp1, setSearchQuery1)
                    }
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-3 h-[40px]">
                <span className="bg-primary text-primary-foreground rounded-full w-6 h-6 flex items-center justify-center text-sm shrink-0">
                  1
                </span>
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    type="text"
                    value={searchQuery1}
                    onChange={(e) => setSearchQuery1(e.target.value)}
                    placeholder="Ex: WhatsApp, Instagram..."
                    className="pl-10 h-[40px]"
                  />
                </div>
              </div>
            )}

            {isSearching1 ? (
              <div className="flex justify-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
              </div>
            ) : (
              searchResults1.length > 0 && (
                <div className="border rounded-lg divide-y max-h-64 overflow-y-auto mt-4">
                  {searchResults1.map((app) => (
                    <div
                      key={app.id}
                      className="p-3 hover:bg-accent/50 cursor-pointer flex items-center gap-3 transition-colors"
                      onClick={() =>
                        selectApp(app, setSelectedApp1, setSearchResults1)
                      }
                    >
                      <img
                        src={app.icon_url}
                        alt={app.name}
                        className="w-10 h-10 rounded-lg"
                      />
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">{app.name}</p>
                        <p className="text-sm text-muted-foreground truncate">
                          {app.developer}
                        </p>
                      </div>
                      <ChevronRight className="h-4 w-4 text-muted-foreground" />
                    </div>
                  ))}
                </div>
              )
            )}
          </CardContent>
        </Card>

        {/* APP 2 */}
        <Card className="hover:shadow-md transition-shadow">
          <CardContent className="p-4">
            {selectedApp2 ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center gap-4">
                  <Link
                    href={`/apps/${selectedApp2.apple_id}`}
                    className="flex items-center gap-4 group flex-1"
                  >
                    <img
                      src={selectedApp2.icon_url}
                      alt={selectedApp2.name}
                      className="w-14 h-14 rounded-xl object-cover border"
                    />
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold truncate group-hover:text-primary transition-colors">
                        {selectedApp2.name}
                      </h3>
                      <p className="text-sm text-muted-foreground truncate">
                        {selectedApp2.developer}
                      </p>
                      <div className="flex gap-1 mt-1">
                        <span className="text-xs bg-accent px-2 py-0.5 rounded">
                          {selectedApp2.category}
                        </span>
                        {selectedApp2.rank && (
                          <span className="text-xs bg-accent px-2 py-0.5 rounded">
                            #{selectedApp2.rank}
                          </span>
                        )}
                      </div>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:text-primary" />
                  </Link>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="shrink-0"
                    onClick={() =>
                      clearSelection(setSelectedApp2, setSearchQuery2)
                    }
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-3 h-[40px]">
                <span className="bg-primary text-primary-foreground rounded-full w-6 h-6 flex items-center justify-center text-sm shrink-0">
                  2
                </span>
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    type="text"
                    value={searchQuery2}
                    onChange={(e) => setSearchQuery2(e.target.value)}
                    placeholder="Ex: TikTok, Facebook..."
                    className="pl-10 h-[40px]"
                  />
                </div>
              </div>
            )}

            {isSearching2 ? (
              <div className="flex justify-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
              </div>
            ) : (
              searchResults2.length > 0 && (
                <div className="border rounded-lg divide-y max-h-64 overflow-y-auto mt-4">
                  {searchResults2.map((app) => (
                    <div
                      key={app.id}
                      className="p-3 hover:bg-accent/50 cursor-pointer flex items-center gap-3 transition-colors"
                      onClick={() =>
                        selectApp(app, setSelectedApp2, setSearchResults2)
                      }
                    >
                      <img
                        src={app.icon_url}
                        alt={app.name}
                        className="w-10 h-10 rounded-lg"
                      />
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">{app.name}</p>
                        <p className="text-sm text-muted-foreground truncate">
                          {app.developer}
                        </p>
                      </div>
                      <ChevronRight className="h-4 w-4 text-muted-foreground" />
                    </div>
                  ))}
                </div>
              )
            )}
          </CardContent>
        </Card>
      </div>

      {/* BOX DE COMPARAÇÃO */}
      {selectedApp1 && selectedApp2 && (
        <Card className="hover:shadow-md transition-shadow">
          {" "}
          <CardHeader className="pb-0">
            <div className="flex items-center gap-2">
              <BarChart2 className="h-5 w-5 text-primary" />
              <CardTitle>Comparison Results</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="px-6 pb-6">
            {" "}
            <div className="overflow-x-auto">
              <Table className="min-w-full">
                <TableHeader className="bg-accent/30">
                  <TableRow>
                    <TableHead className="w-[200px]">Metric</TableHead>
                    <TableHead className="text-center min-w-[180px]">
                      <div className="flex flex-col items-center">
                        <img
                          src={selectedApp1.icon_url}
                          alt={selectedApp1.name}
                          className="w-10 h-10 rounded-lg mb-1"
                        />
                        <span className="font-medium">{selectedApp1.name}</span>
                      </div>
                    </TableHead>
                    <TableHead className="text-center min-w-[180px]">
                      <div className="flex flex-col items-center">
                        <img
                          src={selectedApp2.icon_url}
                          alt={selectedApp2.name}
                          className="w-10 h-10 rounded-lg mb-1"
                        />
                        <span className="font-medium">{selectedApp2.name}</span>
                      </div>
                    </TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {[
                    {
                      name: "Rank",
                      value1: selectedApp1.rank,
                      value2: selectedApp2.rank,
                      format: (v: any) => (v ? `#${v}` : "-"),
                    },
                    {
                      name: "Category",
                      value1: selectedApp1.category,
                      value2: selectedApp2.category,
                    },
                    {
                      name: "List Type",
                      value1: selectedApp1.list_type,
                      value2: selectedApp2.list_type,
                    },
                    {
                      name: "Price",
                      value1:
                        selectedApp1.list_type === "Top Paid"
                          ? selectedApp1.price
                          : "Free",
                      value2:
                        selectedApp2.list_type === "Top Paid"
                          ? selectedApp2.price
                          : "Free",
                    },
                    {
                      name: "Monthly Downloads",
                      value1: selectedApp1.monthly_downloads_estimate,
                      value2: selectedApp2.monthly_downloads_estimate,
                      format: formatCompactNumber,
                    },
                    {
                      name: "Monthly Revenue",
                      value1: selectedApp1.monthly_revenue_estimate,
                      value2: selectedApp2.monthly_revenue_estimate,
                      format: (v: any) =>
                        v ? `$${formatCompactNumber(v)}` : "-",
                    },
                    {
                      name: "Subtitle",
                      value1: selectedApp1.subtitle,
                      value2: selectedApp2.subtitle,
                    },
                  ].map((row, i) => (
                    <TableRow
                      key={i}
                      className={i % 2 === 0 ? "bg-accent/10" : ""}
                    >
                      <TableCell className="font-medium py-3">
                        {row.name}
                      </TableCell>
                      <TableCell className="text-center py-3">
                        {row.format ? row.format(row.value1) : row.value1}
                      </TableCell>
                      <TableCell className="text-center py-3">
                        {row.format ? row.format(row.value2) : row.value2}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
