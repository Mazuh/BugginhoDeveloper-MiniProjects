
-- Implements: https://github.com/BugginhoDeveloper/mini-projeto-1-lua/blob/master/README.md


-- dependencies...
json = require "lib/json"


-- Array of guests list and its length
guests    = { } -- numeric array [number] { name: string, cpf: string, isRemoved: string }
guestsLen = 0 -- zero ins't an avaiable index (lua pattern)

-- local url to persist guests data
PATH_STORAGE = "data/guests.json"

-- OS inner codes
WINDOWS = 1
LINUX   = 2
userOS  = 0 -- for user to select, this script will treat it as Linux by default (use constants for a valid option!)


-- Do some stuff that should be done before run function, like check for OS and data storage file.
function init()

    print("Hi. Select your operational system...")
    print("1 - Windows")
    print("2 - Linux")
    print("So, what's yours?")
    userOS = io.stdin:read()

    print()
    print("Trying to read "..PATH_STORAGE.." (if it doesn't work or it's taking too long, manually create an empty file in this path and/or check scripts permission level)...")
    print()
    if (loadDataFromFile()) then
        print("Previous data found in our files and loaded.")
        printGuests()
    else
        print("There was no data to load. Maybe it's your first time here. Hello there, user!")
    end

    uiWait()
end

-- Run console user interface (for safety exec, call this only after init function)
function run()
    while (true) do
        uiClear()
        print("GUESTS LIST MANAGER\n\n"
            .."Options:\n"
            .."1 - show current guests list\n"
            .."2 - add new guest\n"
            .."3 - search guest by CPF\n"
            .."4 - remove guest by CPF\n"
            .."5 - show removed guests\n"
            .."q - save and quit\n"
            .."c - quit without saving\n"
            .."x - destroy all current data")
        print("What option number will you choose?")
        option = io.stdin:read()

        uiClear()

        if (option == "c") then -- cancel
            print("Just exiting. All your unsaved progress has been lost.")
            os.exit()

        elseif (option == "x") then -- destroy
            print("Oh, a violent one! Trying to delete all data...")
            if (createOrClearFile()) then
                print("Your data has been destroyed.")
            else
                print("Sorry, couldn't be done.")
            end

        elseif (option == "q") then -- save n quit
            print("Trying to save your list...")
            if (saveDataInFile()) then
                print("Saved!\nNow exiting...")
                os.exit()
            else
                print("That's embarrassing, but something went wrong and your list couldn't be saved!")
            end
            
        elseif (option == "1") then -- show list
            print("Showing current guests list...")
            printGuests()

        elseif (option == "2") then -- add guest
            print("Adding new guest...")
            print("What's his full name?")
            local inName = io.stdin:read()
            print("What's his/her CPF?")
            local inCpf = io.stdin:read()

            if (addGuest(inName, inCpf)) then
                print("Successfuly added!")
            else
                print("Something went wrong. Maybe his/her CPF has already been registered and/or has been removed.")
            end
        
        elseif (option == "3") then -- search by CPF
            print("Searching guest by CPF...")
            print("What's his/her CPF?")
            local inCpf = io.stdin:read()

            local outGuest = findGuestByCPF(inCpf)

            if (outGuest) then
                print(outGuest.name)
                if (outGuest.isRemoved) then
                    print("Has been removed for: "..outGuest.isRemoved)
                else
                    print("Present in the current list.")
                end
            else
                print("Sorry. It couldn't been found.")
            end
        
        elseif (option == "4") then -- remove by CPF
            print("Removing guest by CPF...")
            print("What's his/her CPF?")
            local inCpf = io.stdin:read()
            print("Why?")
            local inReason = io.stdin:read()
            
            if (removeGuest(inCpf, inReason)) then
                print("This guest has been removed.")
            else
                print("Nope. Couldn't be done. Maybe this guest has been removed before and/or isn't in the list?")
            end
        
        elseif (option == "5") then -- show removed guests
            print("Showing removed guests...")
            printRemovedGuests()

        else -- idk...?
            print("Sorry, I don't understand what you want!")

        end

        uiWait()

    end
end

-- Clears console user interface
function uiClear()
    if (userOS == WINDOWS) then
        os.execute("cls")
    else
        os.execute("clear")
    end
end

-- Ask user to press Enter to continue and wait for it.
function uiWait()
    print("\nPress Enter to continue...")
    io.stdin:read()
end


-- Create a new guest, add it to list and update the size number.
-- PARAM
--  name : string complete guest name
--  cpf  : string valid personal ID (t: cadastro de pessoa física) formatted as XXX.XXX.XXX-XX
-- RETURN
--  true  : boolean if it worked
--  false : boolean if cpf already exists or if there's an empty param
function addGuest(name, cpf)
    if (findGuestByCPF(cpf) or cpf=="" or name=="") then
        return false
    end
    
    local guest = {
        ['name'] = name,
        ['cpf'] = cpf,
        ['isRemoved'] = nil,
    }
    guestsLen = guestsLen + 1

    table.insert(guests, guest)

    return true
end

-- Remove guest (visibility) from list with a reason (his data is still avaiable by some specific functions)
-- PARAM
--  cpf    : string valid personal ID (t: cadastro de pessoa física) formatted as XXX.XXX.XXX-XX
--  reason : string any text explaining why this guest has been removed
-- RETURN
--  true  : boolean if a guest was found and removed
--  false : boolean if couldn't find this guest or he/she was already been removed
function removeGuest(cpf, reason)
    -- Interesting: this function doesnt copy guest element
    -- but brings a reference for it, so modifying this local var also
    -- will make changes in guests global list.
    local guest = findGuestByCPF(cpf) 
    
    if (guest and not(guest.isRemoved)) then
        guest.isRemoved = reason
        return true
    end

    return false
end

-- Find a guest from list, if it is visible or not (equivalent to: 'removed' or not)
-- PARAM
--  cpf   : string valid personal ID (t: cadastro de pessoa física) formatted as XXX.XXX.XXX-XX
-- RETURN
--  table : element of guests array, if a guest was found
--  false : boolean if couldn't find this guest 
function findGuestByCPF(cpf)
    for i=1, guestsLen do
        if (guests[i].cpf == cpf) then
            return guests[i]
        end
    end

    return false
end

-- Print all non-removed guests in format "Person Name (XXX.XXX.XXX-XX)" 
function printGuests()
    for i=1, guestsLen do
        if (not(guests[i].isRemoved)) then
            print(guests[i].name.." ("..guests[i].cpf..")")
        end
    end
end

-- Print all removed guests in format "Person Name (XXX.XXX.XXX-XX) - Removed for: Some reason" 
function printRemovedGuests()
    for i=1, guestsLen do
        if (guests[i].isRemoved) then
            print(guests[i].name.." ("..guests[i].cpf..") - Removed for: "..guests[i].isRemoved)
        end
    end
end 

-- Decode guests list JSON stored in a local (existent) file PATH_STORAGE, bringing it to var guests.
-- README
--  For some reason, the script enters an undefined loop if the files doesn't even exist, so I created
--  an empty file. There's a function in this script that can clear or create a clared file in the same path.
-- RETURN
--  true  : boolean if it could find, load and decode json file
--  false : boolean if something went wrong (it will likely throw a fatal error) or the file was empty
function loadDataFromFile()
    file = io.open(PATH_STORAGE, "r")

    io.input(file)

    contentFound = io.read()
    
    if (contentFound == "" or contentFound == nil) then
        io.close(file)
        createOrClearFile()
        return false
    end

    guests = json.decode(contentFound)
    io.close(file)
    return true
end

-- Encode guests list into a JSON and stores it in a local file PATH_STORAGE.
-- RETURN
--  true  : boolean if it could encode guests list and save it in the file
--  false : boolean if something went wrong (likely will throw a fatal error)
function saveDataInFile()
    file = io.open(PATH_STORAGE, "w")

    io.output(file)

    if (io.write(json.encode(guests))) then
        io.close(file)
        return true
    end
    
    io.close(file)
    return false
end

-- Try to create an empty file or clear all data in the existent path 
--  true  : boolean if it could save the file
--  false : boolean if something went wrong (likely will throw a fatal error)
function createOrClearFile()
    file = io.open(PATH_STORAGE, "w")

    io.output(file)

    if (io.write()) then
        io.close(file)
        return true
    end
    
    io.close(file)
    return false
end


-- routine algorithms
init()
run()
