on run
	-- Keep selected text and positions out of persistent script state.
	local locLength, selectionLength, locLines, selectionLines, looseSelect, theSelection

	tell application "CotEditor"
		if exists front document then
			tell front document
				if coloring style is not in {"Markdown"} then
					return
				end if
			
				-- get selection's positional data
				set {locLength, selectionLength} to range of selection
				set {locLines, selectionLines} to line range of selection
				set looseSelect to 0
				-- whole lines select
				if (selectionLines is greater than or equal to looseSelect as number) then
					set line range of selection to {locLines, selectionLines}
					set {locLength, selectionLength} to range of selection
				end if
			
				-- ignore last line break
				if contents of selection ends with "\n" then set range of selection to {locLength, selectionLength - 1}
			
				-- get contents
				set theSelection to contents of selection
				if rich text 1 of theSelection is equal to "#" then
					set contents of selection to "#" & theSelection
				else
					set contents of selection to "# " & theSelection
				end if
			end tell
		end if
	end tell
end run
