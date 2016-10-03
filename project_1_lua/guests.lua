
-- Array of guests list and its length
guests = { }
guestsLen = 0

-- Create a new guest, add it to list and update the size number.
-- PARAM
--  name : string complete guest name
--  cpf  : string valid personal ID (t: cadastro de pessoa física) formatted as XXX.XXX.XXX-XX
-- RETURN
--  true  : boolean if it worked
--  false : boolean if something went wrong, like cpf already exists (TODO)
function addGuest(name, cpf)
    local guest = {
        ['name'] = name,
        ['cpf'] = cpf,
        ['isVisible'] = true,
    }
    guestsLen = guestsLen + 1

    table.insert(guests, guest)

    return true
end

function removeGuest(reason)
    -- TODO
end

function getGuestByCPF(cpf)
    -- TODO
end

function getAllGuests()
    -- TODO
end

-- Print all non-removed guests in format "Person Name (XXX.XXX.XXX-XX)" 
function printGuests()
    for i=1, guestsLen do
        if (guests[i].isVisible) then
            print(guests[i].name.." ("..guests[i].cpf..")")
        end
    end
end

-- Print all removed guests in format "Person Name (XXX.XXX.XXX-XX)" 
function printRemovedGuests()
    for i=1, guestsLen do
        if not (guests[i].isVisible) then
            print(guests[i].name.." ("..guests[i].cpf..")")
        end
    end
end 

--addGuest("Um nome", "Um cpf")
--addGuest("Dois nome", "Dois cpf")
--printGuests()
