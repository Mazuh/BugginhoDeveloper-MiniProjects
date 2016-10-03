
-- Implements: https://github.com/BugginhoDeveloper/mini-projeto-1-lua/blob/master/README.md


-- dependencies...
json = require "lib/json"


-- Array of guests list and its length
guests = { } -- numeric array [number] { name: string, cpf: string, isRemoved: string }
guestsLen = 0 -- zero ins't an avaiable index (lua pattern)

-- local url to persist guests data
PATH_STORAGE = "data/guests.json"


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

-- Print all removed guests in format "Person Name (XXX.XXX.XXX-XX)" 
function printRemovedGuests()
    for i=1, guestsLen do
        if (guests[i].isRemoved) then
            print(guests[i].name.." ("..guests[i].cpf..") - Removed for: "..guests[i].isRemoved)
        end
    end
end 

-- Decode guests list JSON stored in a local (existent) file, bringing it to var guests.
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

-- Encode guests list into a JSON and stores it in a local file.
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



-- TESTS

print("Trying to read "..PATH_STORAGE.." (if it doesn't work or it's taking too long, manually create an empty file in this path and/or check scripts permission level)...")
if (loadDataFromFile()) then
    print("Previous data found in our files and loaded.")
    printGuests()
else
    print("There was no data to load.")
end

print()

addGuest("Marcell Guilherme", "000.000.000-11")
addGuest("Yuri Henrique", "000.000.000-22")
print("--> Tried to add 2 guests: Marcell and his minion Yuri")
printGuests()

print()

removeGuest("000.000.000-22", "For being noob")
print("--> Removed: Yuri")
printGuests()

print()

addGuest("Yuri Fake", "000.000.000-11") -- you shall not pass!
addGuest("Italo Vieira", "000.000.000-33")
print("--> Tried to add 2 guests: Yuri (faking Marcell's CPF) and Italo (a regular non-nigga)")
printGuests()

print()

print("--> Printing removed guests and reasons...")
printRemovedGuests()

print()

print("This ends our little journey. Trying to save...")
saveDataInFile()

print()

print("Saved! See ya.")