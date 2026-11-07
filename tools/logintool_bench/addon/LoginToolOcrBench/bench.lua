-- Dev-only benchmark for the WoW Login Tool's character-select OCR.
-- Draws pages of cards that copy CharacterSelectListCharacterTemplate (forever
-- branch: card 347x95, Name GlueFontNormalHuge at 14,-14 size 270x22, Info
-- GlueFontNormalLarge 4 below, Status GlueFontDisableLarge at 14,17 size 215x18)
-- at several pixel-per-unit scales, and records every string with its pixel
-- rectangle in LoginToolOcrBenchDB for the evaluator.
--   /otb start   show page 1 (CTRL-SHIFT-F12 = next page)
--   /otb auto 2  same, but turn the page every 2 s by itself
--   /otb stop    hide; /reload afterwards writes the SavedVariables
local _, ns = ...

local SCALES = { 0.67, 0.8, 1.0, 1.33, 2.0 }
local CARD_W, CARD_H, PITCH_X, PITCH_Y = 347, 95, 372, 100
local TOP, LEFT = 70, 20
local BACKDROPS = {
    "glues-characterselect-card-singles",
    "glues-characterselect-card-selected",
    "glues-characterselect-card-singles-hover",
}

-- CHARACTER_SELECT_INFO is a glue string and missing in game; koKR values from
-- GlobalStrings (CHARACTER_SELECT_INFO 33939, CHARACTER_SELECT_INFO_GHOST 33941)
local INFO = CHARACTER_SELECT_INFO or "%d 레벨 %s"
local INFO_GHOST = CHARACTER_SELECT_INFO_GHOST or "%d 레벨 %s (유령)"

local pw, ph = GetPhysicalScreenSize()
local pages, cards, current = nil, {}, 0
local classes, zones = {}, {}

local root = CreateFrame("Frame", "LoginToolOcrBenchRoot", UIParent)
root:SetAllPoints(UIParent)
root:SetFrameStrata("FULLSCREEN_DIALOG")
root:Hide()
local bg = root:CreateTexture(nil, "BACKGROUND")
bg:SetAllPoints()
bg:SetColorTexture(0.03, 0.03, 0.04, 1)

local marker = root:CreateFontString(nil, "OVERLAY")
marker:SetFont(STANDARD_TEXT_FONT, 26, "")
marker:SetTextColor(1, 1, 1)
marker:SetJustifyH("LEFT")
marker:SetPoint("TOPLEFT", root, "TOPLEFT", 16, -12)

local stage = CreateFrame("Frame", nil, root)
stage:SetPoint("TOPLEFT", root, "TOPLEFT", 0, 0)

local function fontObject(glue, fallback, r, g, b)
    local obj = _G[glue]
    if type(obj) == "table" and obj.GetFont then
        return obj, nil
    end
    return _G[fallback], { r, g, b }
end

local function applyFont(fs, glue, fallback, r, g, b)
    local obj, color = fontObject(glue, fallback, r, g, b)
    fs:SetFontObject(obj)
    if color then
        fs:SetTextColor(color[1], color[2], color[3])
    end
end

local function makeCard(i)
    local c = CreateFrame("Frame", nil, stage)
    c:SetSize(CARD_W, CARD_H)
    c.bg = c:CreateTexture(nil, "BACKGROUND")
    c.bg:SetAllPoints()
    c.name = c:CreateFontString(nil, "OVERLAY")
    applyFont(c.name, "GlueFontNormalHuge", "SystemFont22_Shadow_Outline", 1, 0.78, 0)
    c.name:SetSize(270, 22)
    c.name:SetJustifyH("LEFT")
    c.name:SetPoint("TOPLEFT", 14, -14)
    c.info = c:CreateFontString(nil, "OVERLAY")
    applyFont(c.info, "GlueFontNormalLarge", "SystemFont_Shadow_Outline_Large", 1, 0.82, 0)
    c.info:SetSize(270, 18)
    c.info:SetJustifyH("LEFT")
    c.info:SetPoint("TOPLEFT", c.name, "BOTTOMLEFT", 0, -4)
    c.status = c:CreateFontString(nil, "OVERLAY")
    applyFont(c.status, "GlueFontDisableLarge", "SystemFont_Shadow_Outline_Large", 0.5, 0.5, 0.5)
    c.status:SetSize(215, 18)
    c.status:SetJustifyH("LEFT")
    c.status:SetPoint("BOTTOMLEFT", 14, 17)
    cards[i] = c
    return c
end

local function collectGameData()
    for i = 1, (GetNumClasses and GetNumClasses() or 0) do
        local name, file = GetClassInfo(i)
        if name and file then
            local color = (C_ClassColor and C_ClassColor.GetClassColor(file)) or RAID_CLASS_COLORS[file]
            table.insert(classes, { name = name, file = file, color = color })
        end
    end
    local seen = {}
    if C_Map and C_Map.GetMapInfo then
        for id = 1, 3000 do
            local info = C_Map.GetMapInfo(id)
            if info and info.name and info.name ~= "" and (info.mapType == 3 or info.mapType == 4)
                    and not seen[info.name] then
                seen[info.name] = true
                table.insert(zones, info.name)
            end
        end
    end
    if #zones == 0 then
        zones = { "?" }
    end
end

local function buildPages()
    pages = {}
    local n = #ns.NAMES
    for _, k in ipairs(SCALES) do
        local wUnits, hUnits = pw / k, ph / k
        local cols = math.max(1, math.floor((wUnits - LEFT) / PITCH_X))
        local rows = math.max(1, math.floor((hUnits - TOP / k * 1.0 - 60) / PITCH_Y))
        local per = cols * rows
        local i = 1
        while i <= n do
            table.insert(pages, { k = k, first = i, last = math.min(n, i + per - 1), cols = cols, rows = rows })
            i = i + per
        end
    end
end

local function pxRect(fs)
    local l, b, w, h = fs:GetRect()
    if not l then
        return 0, 0, 0, 0
    end
    local s = fs:GetEffectiveScale() * ph / 768
    if fs ~= marker then
        w = math.min(w, fs:GetStringWidth() + 2)
    else
        w = fs:GetStringWidth()
    end
    return math.floor(l * s), math.floor(ph - (b + h) * s), math.ceil((l + w) * s), math.ceil(ph - b * s)
end

local function record(page, k, role, tag, text, fs)
    local l, t, r, b = pxRect(fs)
    table.insert(LoginToolOcrBenchDB.items,
        table.concat({ page, string.format("%.3f", k), role, tag, text, l, t, r, b }, "\t"))
end

local function showPage(p)
    current = p
    for _, c in ipairs(cards) do
        c:Hide()
    end
    local page = pages[p]
    if not page then
        marker:SetText("DONE")
        return
    end
    local k = page.k
    stage:SetScale((k * 768 / ph) / root:GetEffectiveScale())
    stage:SetSize(pw / k, ph / k)
    marker:SetText("PAGE " .. p)
    local slot = 0
    for idx = page.first, page.last do
        slot = slot + 1
        local c = cards[slot] or makeCard(slot)
        local col, row = (slot - 1) % page.cols, math.floor((slot - 1) / page.cols)
        c:ClearAllPoints()
        c:SetPoint("TOPLEFT", stage, "TOPLEFT", LEFT + col * PITCH_X, -(TOP / k + 30 + row * PITCH_Y))
        local atlas = BACKDROPS[(idx % #BACKDROPS) + 1]
        if not (c.bg.SetAtlas and pcall(c.bg.SetAtlas, c.bg, atlas)) or not c.bg:GetAtlas() then
            c.bg:SetColorTexture(0.13, 0.10, 0.07, 0.95)
        end
        local entry = ns.NAMES[idx]
        c.name:SetText(entry[1])
        local cls = classes[(idx % math.max(1, #classes)) + 1]
        local level = (idx * 37) % 60 + 1
        local fmt = (idx % 9 == 0) and INFO_GHOST or INFO
        local plain, shown = "?", "?"
        if cls then
            plain = fmt:format(level, cls.name)
            shown = cls.color and fmt:format(level, cls.color:WrapTextInColorCode(cls.name)) or plain
        end
        c.info:SetText(shown)
        local zone = zones[(idx % #zones) + 1]
        c.status:SetText(zone)
        c:Show()
        record(p, k, "name", entry[2], entry[1], c.name)
        record(p, k, "info", (cls and cls.file or "?") .. ((idx % 9 == 0) and "_ghost" or ""), plain, c.info)
        record(p, k, "zone", c.status:IsTruncated() and "truncated" or "full", zone, c.status)
    end
    record(p, k, "marker", "-", "PAGE " .. p, marker)
end

local nextButton = CreateFrame("Button", "LoginToolOcrBenchNext", root)
nextButton:SetScript("OnClick", function()
    showPage(current + 1)
end)

local ticker

SLASH_LOGINTOOLOCRBENCH1 = "/otb"
SlashCmdList.LOGINTOOLOCRBENCH = function(msg)
    if ticker then
        ticker:Cancel()
        ticker = nil
    end
    if msg == "stop" then
        ClearOverrideBindings(root)
        root:Hide()
        return
    end
    -- "/otb auto 2": advance every 2 s on its own, so the capture needs no key
    -- presses and the game window does not have to stay in front
    local every = tonumber(msg:match("^auto%s+([%d%.]+)"))
    pw, ph = GetPhysicalScreenSize()
    if #classes == 0 then
        collectGameData()
    end
    buildPages()
    LoginToolOcrBenchDB = { screen = pw .. "x" .. ph, pages = #pages, classes = #classes, zones = #zones, items = {} }
    SetOverrideBindingClick(root, true, "CTRL-SHIFT-F12", "LoginToolOcrBenchNext")
    root:Show()
    showPage(1)
    if every then
        ticker = C_Timer.NewTicker(every, function()
            if current > #pages then
                ticker:Cancel()
                ticker = nil
                return
            end
            showPage(current + 1)
        end)
    end
    print("LoginToolOcrBench: " .. #pages .. " pages, " .. #classes .. " classes, " .. #zones .. " zones")
end
