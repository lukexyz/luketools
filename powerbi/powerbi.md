
# ======================
# PowerBI calendar expression
 # from https://exceleratorbi.com.au/build-reusable-calendar-table-power-query/
let
    Source = List.Dates(StartDate, Length, #duration(1, 0, 0, 0)),
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Renamed Columns" = Table.RenameColumns(#"Converted to Table",{{"Column1", "Date"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Date", type date}}),
    StartDate = #date(2016, 1, 1),
    Today = DateTime.Date(DateTime.LocalNow()),
    Length = Duration.Days(Today - StartDate),
    Custom1 = #"Changed Type",
    #"Inserted Year" = Table.AddColumn(Custom1, "Fin Year", each Date.Year([Date]+#duration(184,0,0,0)), Int64.Type),
    #"Inserted Month Name" = Table.AddColumn(#"Inserted Year", "Month Name", each Date.MonthName([Date]), type text),
    #"Inserted Day Name" = Table.AddColumn(#"Inserted Month Name", "Day Name", each Date.DayOfWeekName([Date]), type text),
    #"Inserted Month" = Table.AddColumn(#"Inserted Day Name", "Fin Month", each if Date.Month([Date]) >=7 then Date.Month([Date])-6 else Date.Month([Date])+6  , Int64.Type),
    #"Inserted Day of Week" = Table.AddColumn(#"Inserted Month", "Day of Week", each Date.DayOfWeek(([Date]), Day.Sunday)+1, Int64.Type),
    #"Inserted First Characters" = Table.AddColumn(#"Inserted Day of Week", "MMM", each Text.Start([Month Name], 3), type text),
    #"Inserted First Characters1" = Table.AddColumn(#"Inserted First Characters", "DDD", each Text.Start([Day Name], 3), type text),
    #"Reordered Columns" = Table.ReorderColumns(#"Inserted First Characters1",{"Date", "Fin Year", "Month Name", "MMM", "Fin Month", "Day Name", "DDD", "Day of Week"}),
    
    #"Added Custom" = Table.AddColumn(#"Reordered Columns", "FYMM", each ([Fin Year]-2000)*100 + [Fin Month]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{{"FYMM", Int64.Type}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type1", "MonthID", each (Date.Year([Date]) - Date.Year(StartDate))*12 + Date.Month([Date])),
    #"Changed Type2" = Table.TransformColumnTypes(#"Added Custom1",{{"MonthID", Int64.Type}})
in
    #"Changed Type2"


# ======================
# DAX Expressions 

# find first instance of " " and replace
new col = SUBSTITUTE([Product_Description], " ", "&", 1)  

# new metrics table (groupby + filter + aggregate function)
Metrics  = SUMMARIZECOLUMNS(DAX_Training_Sales_Transactions[Product_Code]
                          ,DAX_Training_Sales_Transactions[Sales_Date]
                          ,DAX_Training_Sales_Transactions[Channel_Code]
                  ,FILTER(DAX_Training_Sales_Transactions,DAX_Training_Sales_Transactions[Brand_Code] <>"98-21")
                          ,"Sales Count",SUM(DAX_Training_Sales_Transactions[Sales_Qty])
                          ,"Sales euro",(SUM(DAX_Training_Sales_Transactions[Sales Value])))

# new customer table(separate)
Customer = SUMMARIZECOLUMNS(DAX_Training_Sales_Transactions[Customer_Code],
                            DAX_Training_Sales_Transactions[Registration_Date],
                    FILTER(DAX_Training_Sales_Transactions,DAX_Training_Sales_Transactions[Brand_Code] <> "98-21"))



# ======================
# DAX Expressions 


# search for index position of first "-", start position 1, return -1 if not found
Season Gap = SEARCH( "-", [text column], 1, -1)

# cut string left of position
Season = LEFT([text column], number)
# also exist
MID(), RIGHT(), LEN()

# bring in a value from another linked table
RELATED( Customer[Registration_Date])
# and compare
First Day = IF( RELATED( Customer[Registration_Date]) = [Sales_Date], "First Day", "Other")

# grab value from related aggregate table
Total Sales = SUMX(RELATEDTABLE(Metrics), [Sales Count])

COMBINEVALUES("delimiter", col1, col2)


# FORMAT dates
Latest = FORMAT(MAX('Daily Tickets'[DumpDateTime]), "DDD dd MMM yyyy h:nn AM/PM")
month = FORMAT( [sales date], "yyyy-MM")
# ----> or an easier way
date = [ResolvedDateTime].[Date]   # <-- works
month = [ResolvedDateTime].[Month]

# First day of the month
FirstDayofMonth = DATE( YEAR( [Date] ) , MONTH( [Date] ) , 1)
YearMonth = FORMAT( [FilterDate], "MMM" ) & " " & YEAR( [FilterDate] )

## Week start date (monday)
WeekStartDate ='data'[Date] - WEEKDAY([Date],2) + 1


# group field into categories
# Good for quick mapping values in a dict, and you can make a drill down heirachy
right-click column -> group

# better mapping using SWITCH
Product Category = SWITCH( TRUE(), 'Product'[Product] IN {"Shirt", "Tshirt", "blouse", "sweater"}, "Tops",
                                   'Product'[Product] IN {"Trouser", "shorts", "skirt"} , "Bottoms",
                                    "Uncategorised")

# create binned columns
Price Band = SWITCH( TRUE(),
                    [Unit_Price] < 10, "Low",
                    [Unit_Price] < 25, "Medium",
                    [Unit_Price] < 50, "High",
                    [Unit_Price] >= 50, "Premium",
                    "Other")

# sort by column (not numberical, not alpha)
Price Band Sort = SWITCH( TRUE(),
[Unit_Price] < 10, "1",
[Unit_Price] < 25, "2",
[Unit_Price] < 50, "3",
[Unit_Price] >= 50, "4",
"5")
# then
"Column tools" -> "Sort by Column" -> [Price Band Sort]

# DATEDIFF time between dates
ResolutionTime = DATEDIFF([ResolvedDateTime], [CreatedDateTime], MINUTE)
Median Res. Time (mins) = COALESCE(CALCULATE(MEDIAN([ResolutionMinutes]), 'Daily Tickets'[TicketStatus] = "Resolved"), "-")

# FILTER with Dax using variables
Open Requests = COALESCE(COUNTX(FILTER('Daily Tickets', [TicketTypeName] = "Request"), [TicketRef]), 0)


OpenTickets = 
        VAR Notresolved = FILTER('Daily Tickets', [TicketStatus] <> "Resolved")
        VAR Res = COUNTX(Notresolved, [TicketRef])
    RETURN
        IF(ISBLANK(Res), 0, Res)
        
# Simplified version using FILER
OpenTickets2 = COUNTX(FILTER('Daily Tickets', [TicketStatus] <> "Resolved"), [TicketRef])

# CALCULATE
OpenTickets3 = CALCULATE(COUNT('Daily Tickets'[TicketRef]), 
                                'Daily Tickets'[TicketStatus] <> "Resolved")

# CALCULATE with PERSISTENT FILTER using ALL
OpenTickets4 = CALCULATE( COUNT('Daily Tickets'[TicketRef]),
                          FILTER( ALL( 'Daily Tickets'[TicketStatus]), 'Daily Tickets'[TicketStatus] <> "Resolved"))

# COALESCE instead of ISBLANK! removes "(blank)"
Tickets = COALESCE(COUNT([TicketRef]), 0)


# YEAR TO DATE (and comparison to last year)
TicketsYTD = TOTALYTD([Tickets#], 'Calendar'[First Day of Month])
TicketsLastYTD = TOTALYTD([Tickets#], SAMEPERIODLASTYEAR('Calendar'[First Day of Month]))


# STRING duration of time "9 Hours & 5 Minutes" etc
#   look here for more https://radacad.com/calculate-duration-in-days-hours-minutes-and-seconds-dynamically-in-power-bi-using-dax
Database String Duration in Hours and Minutes = 
var vMinues=[DataUpdateTimeDiffMins]
var vHours=int( vMinues/60)
var vRemainingMinutes=MOD(vMinues, 60)
return
  if(vHours<6,
  vHours&" hrs "& vRemainingMinutes& " min",
  vHours&" hrs ")


# Engineer Summary table powerBI
Engineer_Summary = 
SUMMARIZECOLUMNS(
  'Monthly Tickets'[AnalystOwner], 'Monthly Tickets'[ResolvedMonth]
  , FILTER('Monthly Tickets', [FeedbackMonth] > DATE(2020, 06, 01))
  ,"TicketCount", DISTINCTCOUNT('Monthly Tickets'[TicketId])
  ,"ResolvedTicketCount", COUNTX(FILTER('Monthly Tickets', [ResolvedDate] <> BLANK()), [TicketId])
  ,"AvgResolutionSeconds", ROUND(AVERAGEX(FILTER('Monthly Tickets', [InitialToResolveSecs] > 0), 'Monthly Tickets'[InitialToResolveSecs]), 0)
  ,"AvgResolutionHours", ROUND(AVERAGEX(FILTER('Monthly Tickets', [InitialToResolveSecs] > 0), 'Monthly Tickets'[ResolutionTimeInHours]), 1)
  ,"FeedbackScore", ROUND(AVERAGE('Monthly Tickets'[FeedbackScoreRaw]), 2)
  ,"FeedbackCount", COUNTX(FILTER('Monthly Tickets', [FeedbackScoreRaw] > 0), [FeedbackScoreRaw])
  ,"DaysActive", DISTINCTCOUNT('Monthly Tickets'[ResolvedDate])
  ,"FiveStarCount", COUNTX(FILTER('Monthly Tickets', [FeedbackScoreRaw]=5), [FeedbackScoreRaw])
)

# Conditional Title Value
Open Tickets First Day = CALCULATE(SUM(A3_Open_Tickets_Daily[OpenTickets]), FIRSTDATE(A3_Open_Tickets_Daily[DumpDate]))
Open Tickets Latest Day = CALCULATE(SUM(A3_Open_Tickets_Daily[OpenTickets]), LASTDATE(A3_Open_Tickets_Daily[DumpDate]))

Open Tickets Delta = 
VAR val = A3_Open_Tickets_Daily[Open Tickets Latest Day] - A3_Open_Tickets_Daily[Open Tickets First Day]
RETURN IF(val > 0, "(increase of +" & val & ")", "(decrease of -" & val & ")")


Seasonal_Period_XmasNY = IF(AND(A3_Open_Tickets_Daily[DumpDate]>=DATE(2021,12,01), A3_Open_Tickets_Daily[DumpDate]<DATE(2022,02,01)), "NY 2022", 
                            IF(AND(A3_Open_Tickets_Daily[DumpDate]>=DATE(2020,12,01), A3_Open_Tickets_Daily[DumpDate]<DATE(2021,02,01)), "NY 2021",
                            IF(AND(A3_Open_Tickets_Daily[DumpDate]>=DATE(2019,12,01), A3_Open_Tickets_Daily[DumpDate]<DATE(2020,02,01)), "NY 2020",
                            IF(AND(A3_Open_Tickets_Daily[DumpDate]>=DATE(2018,12,01), A3_Open_Tickets_Daily[DumpDate]<DATE(2019,02,01)), "NY 2019",
                            "Other"))))

Created_Seasonal_Period_XmasNY = IF(AND(A1_Created_Tickets_Daily[CreatedDate]>=DATE(2021,12,01), A1_Created_Tickets_Daily[CreatedDate]<DATE(2022,02,01)), "NY 2022", 
                            IF(AND(A1_Created_Tickets_Daily[CreatedDate]>=DATE(2020,12,01), A1_Created_Tickets_Daily[CreatedDate]<DATE(2021,02,01)), "NY 2021",
                            IF(AND(A1_Created_Tickets_Daily[CreatedDate]>=DATE(2019,12,01), A1_Created_Tickets_Daily[CreatedDate]<DATE(2020,02,01)), "NY 2020",
                            IF(AND(A1_Created_Tickets_Daily[CreatedDate]>=DATE(2018,12,01), A1_Created_Tickets_Daily[CreatedDate]<DATE(2019,02,01)), "NY 2019",
                            "Other"))))


In_Progress_Hours_4 = IF(CEILING(SD_DailyTickets[In_Progress_Time], 240) < 60*24*4, CEILING(SD_DailyTickets[In_Progress_Time], 240), 60*24*4)

Client_ICAN = IF('SD_DailyTickets'[EmailDomain]="dawnhouse-ican.notts.sch.uk", "Dawn House", 
            IF('SD_DailyTickets'[EmailDomain]="meath-ican.org.uk", "Meath and Central",
            IF('SD_DailyTickets'[EmailDomain]="ican.org.uk", "Meath and Central", "Other")))



## SELECTEDVALUE
# Returns the value when the context for columnName has been filtered down to one distinct value only. Otherwise returns alternateResult.
SelectedClient = IF(ISBlank(SELECTEDVALUE('Customer Table'[ClientName])), "All Clients", SELECTEDVALUE('Customer Table'[ClientName]) )


## Engineer Summary Backup DAX
Engineer_Summary = 
SUMMARIZECOLUMNS(
  'Monthly Tickets'[AnalystOwner], 'Monthly Tickets'[ResolvedMonth]
  , FILTER('Monthly Tickets', [FeedbackMonth] > DATE(2020, 06, 01))
  ,"TicketCount", DISTINCTCOUNT('Monthly Tickets'[TicketId])
  ,"ResolvedTicketCount", COUNTX(FILTER('Monthly Tickets', [ResolvedDate] <> BLANK()), [TicketId])
  ,"AvgResolutionSeconds", ROUND(AVERAGEX(FILTER('Monthly Tickets', [InitialToResolveSecs] > 0), 'Monthly Tickets'[InitialToResolveSecs]), 0)
  ,"AvgResolutionHours", ROUND(AVERAGEX(FILTER('Monthly Tickets', [InitialToResolveSecs] > 0), 'Monthly Tickets'[ResolutionTimeInHours]), 1)
  ,"FeedbackScore", ROUND(AVERAGE('Monthly Tickets'[FeedbackScoreRaw]), 2)
  ,"FeedbackCount", COUNTX(FILTER('Monthly Tickets', [FeedbackScoreRaw] > 0), [FeedbackScoreRaw])
  ,"DaysActive", DISTINCTCOUNT('Monthly Tickets'[ResolvedDay])
  ,"FiveStarCount", COUNTX(FILTER('Monthly Tickets', [FeedbackScoreRaw]=5), [FeedbackScoreRaw])
)

# DAX Variables in return
Sales YoY Growth =
VAR SalesPriorYear =
    CALCULATE ( [Sales], PARALLELPERIOD ( 'Date'[Date], -12, MONTH ) )
VAR SalesVariance =
    DIVIDE ( ( [Sales] - SalesPriorYear ), SalesPriorYear )
RETURN
    SalesVariance


# Measure to take text from selected filters
SelectedClient = SELECTEDVALUE('Customer Table'[ClientName], "Selected Clients")


# PowerBi Background colour (off-white)
#F8FAFC

# PowerBi App Link
https://app.powerbi.com/Redirect?action=OpenApp&appId=16fb56b9-5bf4-4753-9b96-56503a35a47d&ctid=293ebca0-d258-46e7-92ab-615fff9de58d

OpenHours = DATEDIFF([CreatedDateTime], (IF ([ResolvedDateTime]=BLANK(), NOW(), [ResolvedDateTime])), HOUR)


_Open_Tickets = CALCULATE(COUNTX(FILTER(SD_DailyTickets, SD_DailyTickets[TicketStatus]<>"Resolved", SD_DailyTickets[Ticket is Child]<>"Child Ticket"), SD_DailyTickets[TicketId])))