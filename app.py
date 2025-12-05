from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# ملف لحفظ البيانات
DATA_FILE = "tools_data.json"

# تحميل البيانات عند البدء
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# حفظ البيانات
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Endpoint لحفظ الأدوات
@app.route('/save-tools', methods=['POST'])
def save_tools():
    try:
        data = request.json
        player_name = data.get('player', 'default')
        tools = data.get('tools', [])
        
        all_data = load_data()
        all_data[player_name] = tools
        save_data(all_data)
        
        return jsonify({'success': True, 'message': 'تم الحفظ بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Endpoint لاسترجاع الأدوات
@app.route('/get-tools/<player_name>', methods=['GET'])
def get_tools(player_name):
    try:
        all_data = load_data()
        tools = all_data.get(player_name, [])
        return jsonify({'success': True, 'tools': tools})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Endpoint لعرض جميع البيانات
@app.route('/all-players', methods=['GET'])
def all_players():
    try:
        all_data = load_data()
        return jsonify({'success': True, 'data': all_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Endpoint للتحقق من الحالة
@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Server is running ✅', 'version': '1.0'})

# Endpoint لعودة الـ Lua Script
@app.route('/script.lua', methods=['GET'])
def get_script():
    script_content = '''local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")
local LocalPlayer = Players.LocalPlayer

pcall(function()
    print("استهلال الواجهة...")
    
    local ScreenGui = Instance.new("ScreenGui")
    ScreenGui.Name = "PhoneGUI"
    ScreenGui.Parent = CoreGui
    ScreenGui.ResetOnSpawn = false

    local PhoneFrame = Instance.new("Frame")
    PhoneFrame.Size = UDim2.new(0, 180, 0, 340)
    PhoneFrame.Position = UDim2.new(0.5, -90, 0.5, -170)
    PhoneFrame.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    PhoneFrame.BorderSizePixel = 0
    PhoneFrame.Draggable = true
    PhoneFrame.Active = true
    PhoneFrame.Parent = ScreenGui

    local phoneCorner = Instance.new("UICorner")
    phoneCorner.CornerRadius = UDim.new(0, 20)
    phoneCorner.Parent = PhoneFrame

    local HeaderBar = Instance.new("Frame")
    HeaderBar.Size = UDim2.new(1, 0, 0, 35)
    HeaderBar.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    HeaderBar.BorderSizePixel = 0
    HeaderBar.Parent = PhoneFrame

    local MinimizeBtn = Instance.new("TextButton")
    MinimizeBtn.Size = UDim2.new(0, 25, 0, 25)
    MinimizeBtn.Position = UDim2.new(0, 5, 0, 5)
    MinimizeBtn.Text = "−"
    MinimizeBtn.BackgroundColor3 = Color3.fromRGB(100, 100, 0)
    MinimizeBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    MinimizeBtn.Font = Enum.Font.SourceSansBold
    MinimizeBtn.TextSize = 16
    MinimizeBtn.BorderSizePixel = 0
    MinimizeBtn.Parent = HeaderBar

    local RefreshBtn = Instance.new("TextButton")
    RefreshBtn.Size = UDim2.new(0, 25, 0, 25)
    RefreshBtn.Position = UDim2.new(0.5, -12, 0, 5)
    RefreshBtn.Text = "🔄"
    RefreshBtn.BackgroundColor3 = Color3.fromRGB(0, 120, 180)
    RefreshBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    RefreshBtn.Font = Enum.Font.SourceSansBold
    RefreshBtn.TextSize = 12
    RefreshBtn.BorderSizePixel = 0
    RefreshBtn.Parent = HeaderBar

    local CloseBtn = Instance.new("TextButton")
    CloseBtn.Size = UDim2.new(0, 25, 0, 25)
    CloseBtn.Position = UDim2.new(1, -30, 0, 5)
    CloseBtn.Text = "✕"
    CloseBtn.BackgroundColor3 = Color3.fromRGB(200, 50, 50)
    CloseBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    CloseBtn.Font = Enum.Font.SourceSansBold
    CloseBtn.TextSize = 14
    CloseBtn.BorderSizePixel = 0
    CloseBtn.Parent = HeaderBar

    local HomeFrame = Instance.new("Frame")
    HomeFrame.Size = UDim2.new(1, 0, 1, -35)
    HomeFrame.Position = UDim2.new(0, 0, 0, 35)
    HomeFrame.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    HomeFrame.BorderSizePixel = 0
    HomeFrame.Parent = PhoneFrame

    local HomeTitle = Instance.new("TextLabel")
    HomeTitle.Size = UDim2.new(1, 0, 0, 40)
    HomeTitle.Position = UDim2.new(0, 0, 0, 10)
    HomeTitle.Text = "التطبيقات"
    HomeTitle.TextColor3 = Color3.fromRGB(255, 255, 255)
    HomeTitle.BackgroundTransparency = 1
    HomeTitle.Font = Enum.Font.SourceSansBold
    HomeTitle.TextSize = 16
    HomeTitle.Parent = HomeFrame

    local IconContainer = Instance.new("Frame")
    IconContainer.Size = UDim2.new(1, 0, 1, -60)
    IconContainer.Position = UDim2.new(0, 0, 0, 50)
    IconContainer.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    IconContainer.BorderSizePixel = 0
    IconContainer.Parent = HomeFrame

    local PlayersIcon = Instance.new("TextButton")
    PlayersIcon.Size = UDim2.new(0, 70, 0, 90)
    PlayersIcon.Position = UDim2.new(0.5, -45, 0, 10)
    PlayersIcon.Text = "👥"
    PlayersIcon.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    PlayersIcon.Font = Enum.Font.SourceSansBold
    PlayersIcon.TextSize = 35
    PlayersIcon.BorderSizePixel = 0
    PlayersIcon.Parent = IconContainer

    local iconCorner = Instance.new("UICorner")
    iconCorner.CornerRadius = UDim.new(0, 15)
    iconCorner.Parent = PlayersIcon

    local iconLabel = Instance.new("TextLabel")
    iconLabel.Size = UDim2.new(1, 0, 0, 20)
    iconLabel.Position = UDim2.new(0, 0, 1, 2)
    iconLabel.Text = "الأشخاص"
    iconLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
    iconLabel.BackgroundTransparency = 1
    iconLabel.Font = Enum.Font.SourceSans
    iconLabel.TextSize = 9
    iconLabel.Parent = PlayersIcon

    local AccountIcon = Instance.new("TextButton")
    AccountIcon.Size = UDim2.new(0, 70, 0, 90)
    AccountIcon.Position = UDim2.new(0.5, 25, 0, 10)
    AccountIcon.Text = "👤"
    AccountIcon.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    AccountIcon.Font = Enum.Font.SourceSansBold
    AccountIcon.TextSize = 35
    AccountIcon.BorderSizePixel = 0
    AccountIcon.Parent = IconContainer

    local accountCorner = Instance.new("UICorner")
    accountCorner.CornerRadius = UDim.new(0, 15)
    accountCorner.Parent = AccountIcon

    local accountLabel = Instance.new("TextLabel")
    accountLabel.Size = UDim2.new(1, 0, 0, 20)
    accountLabel.Position = UDim2.new(0, 0, 1, 2)
    accountLabel.Text = "حسابي"
    accountLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
    accountLabel.BackgroundTransparency = 1
    accountLabel.Font = Enum.Font.SourceSans
    accountLabel.TextSize = 9
    accountLabel.Parent = AccountIcon

    local SettingsIcon = Instance.new("TextButton")
    SettingsIcon.Size = UDim2.new(0, 70, 0, 90)
    SettingsIcon.Position = UDim2.new(0.5, 25, 0, 110)
    SettingsIcon.Text = "⚙️"
    SettingsIcon.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    SettingsIcon.Font = Enum.Font.SourceSansBold
    SettingsIcon.TextSize = 35
    SettingsIcon.BorderSizePixel = 0
    SettingsIcon.Parent = IconContainer

    local settingsCorner = Instance.new("UICorner")
    settingsCorner.CornerRadius = UDim.new(0, 15)
    settingsCorner.Parent = SettingsIcon

    local settingsLabel = Instance.new("TextLabel")
    settingsLabel.Size = UDim2.new(1, 0, 0, 20)
    settingsLabel.Position = UDim2.new(0, 0, 1, 2)
    settingsLabel.Text = "الإعدادات"
    settingsLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
    settingsLabel.BackgroundTransparency = 1
    settingsLabel.Font = Enum.Font.SourceSans
    settingsLabel.TextSize = 9
    settingsLabel.Parent = SettingsIcon

    local ESPIcon = Instance.new("TextButton")
    ESPIcon.Size = UDim2.new(0, 70, 0, 90)
    ESPIcon.Position = UDim2.new(0.5, -45, 0, 110)
    ESPIcon.Text = "📡"
    ESPIcon.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    ESPIcon.Font = Enum.Font.SourceSansBold
    ESPIcon.TextSize = 35
    ESPIcon.BorderSizePixel = 0
    ESPIcon.Parent = IconContainer

    local espCorner = Instance.new("UICorner")
    espCorner.CornerRadius = UDim.new(0, 15)
    espCorner.Parent = ESPIcon

    local espLabel = Instance.new("TextLabel")
    espLabel.Size = UDim2.new(1, 0, 0, 20)
    espLabel.Position = UDim2.new(0, 0, 1, 2)
    espLabel.Text = "الرادار"
    espLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
    espLabel.BackgroundTransparency = 1
    espLabel.Font = Enum.Font.SourceSans
    espLabel.TextSize = 9
    espLabel.Parent = ESPIcon

    local MainFrame = Instance.new("Frame")
    MainFrame.Size = UDim2.new(1, 0, 1, -35)
    MainFrame.Position = UDim2.new(0, 0, 0, 35)
    MainFrame.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
    MainFrame.Visible = false
    MainFrame.BorderSizePixel = 0
    MainFrame.Parent = PhoneFrame

    local Title = Instance.new("TextLabel")
    Title.Size = UDim2.new(1, 0, 0, 35)
    Title.Text = "👥 اللاعبين"
    Title.TextColor3 = Color3.fromRGB(255, 255, 255)
    Title.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    Title.Font = Enum.Font.SourceSansBold
    Title.TextSize = 14
    Title.BorderSizePixel = 0
    Title.Parent = MainFrame

    local BackBtn = Instance.new("TextButton")
    BackBtn.Size = UDim2.new(0, 25, 0, 25)
    BackBtn.Position = UDim2.new(0, 5, 0, 5)
    BackBtn.Text = "◀"
    BackBtn.BackgroundColor3 = Color3.fromRGB(100, 100, 100)
    BackBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
    BackBtn.Font = Enum.Font.SourceSansBold
    BackBtn.TextSize = 12
    BackBtn.BorderSizePixel = 0
    BackBtn.Parent = MainFrame

    local PlayersCount = Instance.new("TextLabel")
    PlayersCount.Size = UDim2.new(1, 0, 0, 40)
    PlayersCount.Position = UDim2.new(0, 0, 0, 35)
    PlayersCount.Text = "0"
    PlayersCount.TextColor3 = Color3.fromRGB(100, 255, 100)
    PlayersCount.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
    PlayersCount.Font = Enum.Font.SourceSansBold
    PlayersCount.TextSize = 28
    PlayersCount.BorderSizePixel = 0
    PlayersCount.Parent = MainFrame

    local PlayersList = Instance.new("ScrollingFrame")
    PlayersList.Size = UDim2.new(1, -6, 1, -80)
    PlayersList.Position = UDim2.new(0, 3, 0, 75)
    PlayersList.CanvasSize = UDim2.new(0, 0, 0, 0)
    PlayersList.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
    PlayersList.ScrollBarThickness = 4
    PlayersList.BorderSizePixel = 0
    PlayersList.Parent = MainFrame

    local ProfileFrame = nil
    local SettingsFrame = nil
    local ESPActive = false
    local ESPHighlights = {}
    local ESPHitboxes = {}
    local hitboxSize = 1
    local ESPHitboxMultiplier = 1.5
    
    local teamColors = {
        ["Red"] = Color3.fromRGB(255, 50, 50),
        ["Blue"] = Color3.fromRGB(50, 150, 255),
        ["Green"] = Color3.fromRGB(50, 255, 50),
        ["Yellow"] = Color3.fromRGB(255, 255, 50),
        ["Purple"] = Color3.fromRGB(200, 50, 255),
        ["Orange"] = Color3.fromRGB(255, 150, 0),
        ["Pink"] = Color3.fromRGB(255, 50, 200),
        ["Cyan"] = Color3.fromRGB(50, 255, 255),
    }
    
    local function getTeamColor(player)
        if player.Team then
            local teamName = player.Team.Name
            if teamColors[teamName] then
                return teamColors[teamName]
            end
            -- محاولة استخدام TeamColor إذا كان متوفراً
            local success, color = pcall(function()
                return player.Team.TeamColor.Color
            end)
            if success and color then
                return color
            end
        end
        return Color3.fromRGB(200, 200, 200)
    end

    local function createESPHighlights()
        -- حذف جميع الأضواء القديمة
        for player, highlight in pairs(ESPHighlights) do
            if highlight and highlight.Parent then
                pcall(function() highlight:Destroy() end)
            end
        end
        ESPHighlights = {}
        
        -- إخفاء الهيت بوكس القديمة واستعادة خصائصها
        for _, hitbox in ipairs(ESPHitboxes) do
            if hitbox.part and hitbox.part.Parent then
                pcall(function()
                    hitbox.part.Transparency = hitbox.originalTransparency
                    hitbox.part.Color = hitbox.originalColor
                    hitbox.part.CanCollide = hitbox.originalCanCollide
                    hitbox.part.Size = hitbox.originalSize
                end)
            end
        end
        ESPHitboxes = {}
        
        -- إنشاء أضواء جديدة لجميع الأشخاص (حتى المخفيين)
        local players = Players:GetPlayers()
        for _, player in ipairs(players) do
            if player ~= LocalPlayer then
                task.spawn(function()
                    pcall(function()
                        -- محاولة الكشف حتى لو لم تحمّل الشخصية بعد
                        for attempt = 1, 10 do
                            local character = player.Character
                            if not character or not character.Parent then
                                return
                            end
                            
                            -- محاولة إيجاد أي جزء من أجزاء الجسم
                            local found = false
                            local targetPart = nil
                            
                            for _, part in ipairs(character:GetDescendants()) do
                                if part:IsA("BasePart") then
                                    found = true
                                    targetPart = character
                                    break
                                end
                            end
                            
                            if found and character and character.Parent then
                                -- إنشاء الـ Highlight حتى بدون HumanoidRootPart
                                local teamColor = getTeamColor(player)
                                local highlight = Instance.new("Highlight")
                                highlight.Adornee = character
                                highlight.FillColor = teamColor
                                highlight.OutlineColor = teamColor
                                highlight.FillTransparency = 0.3
                                highlight.OutlineTransparency = 0
                                highlight.Parent = character
                                ESPHighlights[player] = highlight
                                
                                -- إظهار جميع الأجزاء
                                for _, part in ipairs(character:GetDescendants()) do
                                    if part:IsA("BasePart") then
                                        local hitboxEntry = {
                                            part = part,
                                            originalTransparency = part.Transparency,
                                            originalColor = part.Color,
                                            originalCanCollide = part.CanCollide,
                                            originalSize = part.Size
                                        }
                                        table.insert(ESPHitboxes, hitboxEntry)
                                        
                                        part.Color = Color3.fromRGB(180, 180, 180)
                                        part.Transparency = 0.75
                                        part.CanCollide = false
                                        
                                        if hitboxSize > 1 then
                                            part.Size = hitboxEntry.originalSize * hitboxSize
                                        end
                                    end
                                end
                                return
                            end
                            
                            -- انتظر قبل المحاولة القادمة
                            if attempt < 10 then
                                task.wait(0.2)
                            end
                        end
                    end)
                end)
            end
        end
    end

    local function toggleESP()
        ESPActive = not ESPActive
        
        if ESPActive then
            ESPIcon.BackgroundColor3 = Color3.fromRGB(100, 50, 50)
            -- تفعيل تكبير الهيت بوكس مع الرادار
            hitboxSize = ESPHitboxMultiplier
            createESPHighlights()
            
            -- استماع لدخول لاعبين جدد
            local playerAddedConnection
            playerAddedConnection = Players.PlayerAdded:Connect(function(player)
                if ESPActive and PhoneFrame and PhoneFrame.Parent then
                    -- تحديث الرادار فوراً عند دخول لاعب جديد
                    task.wait(0.5)
                    createESPHighlights()
                end
            end)
            
            task.spawn(function()
                while ESPActive and PhoneFrame and PhoneFrame.Parent do
                    task.wait(3)
                    if ESPActive then
                        createESPHighlights()
                    end
                end
                -- قطع الاتصال عند إيقاف الـ ESP
                if playerAddedConnection then
                    playerAddedConnection:Disconnect()
                end
            end)
        else
            ESPIcon.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
            hitboxSize = 1
            for player, highlight in pairs(ESPHighlights) do
                if highlight and highlight.Parent then
                    highlight:Destroy()
                end
            end
            ESPHighlights = {}
            
            -- استعادة الخصائص الأصلية للهيت بوكس
            for _, hitbox in ipairs(ESPHitboxes) do
                if hitbox.part and hitbox.part.Parent then
                    hitbox.part.Transparency = hitbox.originalTransparency
                    hitbox.part.Color = hitbox.originalColor
                    hitbox.part.CanCollide = hitbox.originalCanCollide
                    hitbox.part.Size = hitbox.originalSize
                end
            end
            ESPHitboxes = {}
        end
    end

    local function switchToHome()
        MainFrame.Visible = false
        if ProfileFrame then ProfileFrame.Visible = false end
        if SettingsFrame then SettingsFrame.Visible = false end
        HomeFrame.Visible = true
    end

    local function createProfileFrame()
        if ProfileFrame then return end
        
        ProfileFrame = Instance.new("Frame")
        ProfileFrame.Size = UDim2.new(1, 0, 1, -35)
        ProfileFrame.Position = UDim2.new(0, 0, 0, 35)
        ProfileFrame.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
        ProfileFrame.Visible = false
        ProfileFrame.BorderSizePixel = 0
        ProfileFrame.Parent = PhoneFrame

        local ProfileTitle = Instance.new("TextLabel")
        ProfileTitle.Size = UDim2.new(1, 0, 0, 35)
        ProfileTitle.Text = "👤 حسابي"
        ProfileTitle.TextColor3 = Color3.fromRGB(255, 255, 255)
        ProfileTitle.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
        ProfileTitle.Font = Enum.Font.SourceSansBold
        ProfileTitle.TextSize = 14
        ProfileTitle.BorderSizePixel = 0
        ProfileTitle.Parent = ProfileFrame

        local ProfileBackBtn = Instance.new("TextButton")
        ProfileBackBtn.Size = UDim2.new(0, 25, 0, 25)
        ProfileBackBtn.Position = UDim2.new(0, 5, 0, 5)
        ProfileBackBtn.Text = "◀"
        ProfileBackBtn.BackgroundColor3 = Color3.fromRGB(100, 100, 100)
        ProfileBackBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
        ProfileBackBtn.Font = Enum.Font.SourceSansBold
        ProfileBackBtn.TextSize = 12
        ProfileBackBtn.BorderSizePixel = 0
        ProfileBackBtn.Parent = ProfileFrame
        
        ProfileBackBtn.MouseButton1Click:Connect(function()
            switchToHome()
        end)

        local ProfileContent = Instance.new("ScrollingFrame")
        ProfileContent.Size = UDim2.new(1, -6, 1, -40)
        ProfileContent.Position = UDim2.new(0, 3, 0, 40)
        ProfileContent.CanvasSize = UDim2.new(0, 0, 0, 200)
        ProfileContent.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        ProfileContent.ScrollBarThickness = 4
        ProfileContent.BorderSizePixel = 0
        ProfileContent.Parent = ProfileFrame

        local profileInfos = {
            {label = "📝 الاسم:", value = LocalPlayer.Name},
            {label = "🆔 UserID:", value = tostring(LocalPlayer.UserId)},
            {label = "⏰ وقت الدخول:", value = os.date("%Y-%m-%d %H:%M:%S")},
        }

        local yPos = 0
        for _, info in ipairs(profileInfos) do
            local infoLabel = Instance.new("TextLabel")
            infoLabel.Size = UDim2.new(1, 0, 0, 50)
            infoLabel.Position = UDim2.new(0, 0, 0, yPos)
            infoLabel.Text = info.label .. "\\n" .. info.value
            infoLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
            infoLabel.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
            infoLabel.Font = Enum.Font.SourceSans
            infoLabel.TextSize = 11
            infoLabel.TextWrapped = true
            infoLabel.BorderSizePixel = 0
            infoLabel.Parent = ProfileContent
            yPos = yPos + 55
        end
    end

    local MinimizedIcon = Instance.new("TextButton")
    MinimizedIcon.Size = UDim2.new(0, 50, 0, 50)
    MinimizedIcon.Position = UDim2.new(0, 10, 1, -60)
    MinimizedIcon.Text = "📱"
    MinimizedIcon.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    MinimizedIcon.TextColor3 = Color3.fromRGB(255, 255, 255)
    MinimizedIcon.Font = Enum.Font.SourceSansBold
    MinimizedIcon.TextSize = 24
    MinimizedIcon.Visible = false
    MinimizedIcon.ZIndex = 10
    MinimizedIcon.BorderSizePixel = 0
    MinimizedIcon.Parent = ScreenGui

    local minIconCorner = Instance.new("UICorner")
    minIconCorner.CornerRadius = UDim.new(0, 10)
    minIconCorner.Parent = MinimizedIcon

    local function switchToPlayers()
        HomeFrame.Visible = false
        MainFrame.Visible = true
        if ProfileFrame then ProfileFrame.Visible = false end
    end

    local function switchToProfile()
        if not ProfileFrame then createProfileFrame() end
        HomeFrame.Visible = false
        MainFrame.Visible = false
        ProfileFrame.Visible = true
    end

    local function toggleMinimize()
        PhoneFrame.Visible = not PhoneFrame.Visible
        MinimizedIcon.Visible = not MinimizedIcon.Visible
    end

    local function switchToTools()
        if not ToolsFrame then createToolsFrame() end
        HomeFrame.Visible = false
        MainFrame.Visible = false
        if ProfileFrame then ProfileFrame.Visible = false end
        if SettingsFrame then SettingsFrame.Visible = false end
        ToolsFrame.Visible = true
    end

    local jumpLabel = nil
    local jumpSlider = nil
    local speedLabel = nil
    local speedSlider = nil
    local hitboxLabel = nil
    local hitboxSlider = nil

    local function createSettingsFrame()
        if SettingsFrame then return end
        
        SettingsFrame = Instance.new("Frame")
        SettingsFrame.Size = UDim2.new(1, 0, 1, -35)
        SettingsFrame.Position = UDim2.new(0, 0, 0, 35)
        SettingsFrame.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
        SettingsFrame.Visible = false
        SettingsFrame.BorderSizePixel = 0
        SettingsFrame.Parent = PhoneFrame

        local SettingsTitle = Instance.new("TextLabel")
        SettingsTitle.Size = UDim2.new(1, 0, 0, 35)
        SettingsTitle.Text = "⚙️ الإعدادات"
        SettingsTitle.TextColor3 = Color3.fromRGB(255, 255, 255)
        SettingsTitle.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
        SettingsTitle.Font = Enum.Font.SourceSansBold
        SettingsTitle.TextSize = 14
        SettingsTitle.BorderSizePixel = 0
        SettingsTitle.Parent = SettingsFrame

        local SettingsBackBtn = Instance.new("TextButton")
        SettingsBackBtn.Size = UDim2.new(0, 25, 0, 25)
        SettingsBackBtn.Position = UDim2.new(0, 5, 0, 5)
        SettingsBackBtn.Text = "◀"
        SettingsBackBtn.BackgroundColor3 = Color3.fromRGB(100, 100, 100)
        SettingsBackBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
        SettingsBackBtn.Font = Enum.Font.SourceSansBold
        SettingsBackBtn.TextSize = 12
        SettingsBackBtn.BorderSizePixel = 0
        SettingsBackBtn.Parent = SettingsFrame
        
        SettingsBackBtn.MouseButton1Click:Connect(function()
            switchToHome()
        end)

        local SettingsContent = Instance.new("ScrollingFrame")
        SettingsContent.Size = UDim2.new(1, -6, 1, -40)
        SettingsContent.Position = UDim2.new(0, 3, 0, 40)
        SettingsContent.CanvasSize = UDim2.new(0, 0, 0, 380)
        SettingsContent.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
        SettingsContent.ScrollBarThickness = 4
        SettingsContent.BorderSizePixel = 0
        SettingsContent.Parent = SettingsFrame

        -- الحصول على قيمة القفز الحقيقية من اللاعب
        local currentJumpHeight = 50
        if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
            local humanoid = LocalPlayer.Character.Humanoid
            local success = pcall(function()
                currentJumpHeight = humanoid.JumpHeight
            end)
            if not success then
                pcall(function()
                    currentJumpHeight = humanoid.JumpPower
                end)
            end
        end

        jumpLabel = Instance.new("TextLabel")
        jumpLabel.Size = UDim2.new(1, 0, 0, 35)
        jumpLabel.Position = UDim2.new(0, 5, 0, 10)
        jumpLabel.Text = "ارتفاع القفز: " .. tostring(math.floor(currentJumpHeight))
        jumpLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
        jumpLabel.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
        jumpLabel.Font = Enum.Font.SourceSans
        jumpLabel.TextSize = 12
        jumpLabel.TextWrapped = true
        jumpLabel.BorderSizePixel = 0
        jumpLabel.Parent = SettingsContent

        jumpSlider = Instance.new("TextBox")
        jumpSlider.Size = UDim2.new(0.8, 0, 0, 30)
        jumpSlider.Position = UDim2.new(0.1, 0, 0, 50)
        jumpSlider.Text = tostring(math.floor(currentJumpHeight))
        jumpSlider.TextColor3 = Color3.fromRGB(255, 255, 255)
        jumpSlider.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
        jumpSlider.Font = Enum.Font.SourceSans
        jumpSlider.TextSize = 12
        jumpSlider.BorderSizePixel = 0
        jumpSlider.Parent = SettingsContent

        -- الحصول على قيمة السرعة الحقيقية من اللاعب
        local currentSpeed = 16
        if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
            currentSpeed = LocalPlayer.Character.Humanoid.WalkSpeed
        end

        speedLabel = Instance.new("TextLabel")
        speedLabel.Size = UDim2.new(1, 0, 0, 35)
        speedLabel.Position = UDim2.new(0, 5, 0, 95)
        speedLabel.Text = "السرعة: " .. tostring(math.floor(currentSpeed))
        speedLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
        speedLabel.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
        speedLabel.Font = Enum.Font.SourceSans
        speedLabel.TextSize = 12
        speedLabel.TextWrapped = true
        speedLabel.BorderSizePixel = 0
        speedLabel.Parent = SettingsContent

        speedSlider = Instance.new("TextBox")
        speedSlider.Size = UDim2.new(0.8, 0, 0, 30)
        speedSlider.Position = UDim2.new(0.1, 0, 0, 135)
        speedSlider.Text = tostring(math.floor(currentSpeed))
        speedSlider.TextColor3 = Color3.fromRGB(255, 255, 255)
        speedSlider.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
        speedSlider.Font = Enum.Font.SourceSans
        speedSlider.TextSize = 12
        speedSlider.BorderSizePixel = 0
        speedSlider.Parent = SettingsContent

        hitboxLabel = Instance.new("TextLabel")
        hitboxLabel.Size = UDim2.new(1, 0, 0, 35)
        hitboxLabel.Position = UDim2.new(0, 5, 0, 180)
        hitboxLabel.Text = "حجم الهيت بوكس: 1"
        hitboxLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
        hitboxLabel.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
        hitboxLabel.Font = Enum.Font.SourceSans
        hitboxLabel.TextSize = 12
        hitboxLabel.TextWrapped = true
        hitboxLabel.BorderSizePixel = 0
        hitboxLabel.Parent = SettingsContent

        hitboxSlider = Instance.new("TextBox")
        hitboxSlider.Size = UDim2.new(0.8, 0, 0, 30)
        hitboxSlider.Position = UDim2.new(0.1, 0, 0, 220)
        hitboxSlider.Text = "1"
        hitboxSlider.TextColor3 = Color3.fromRGB(255, 255, 255)
        hitboxSlider.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
        hitboxSlider.Font = Enum.Font.SourceSans
        hitboxSlider.TextSize = 12
        hitboxSlider.BorderSizePixel = 0
        hitboxSlider.Parent = SettingsContent

        local applyBtn = Instance.new("TextButton")
        applyBtn.Size = UDim2.new(0.8, 0, 0, 35)
        applyBtn.Position = UDim2.new(0.1, 0, 0, 265)
        applyBtn.Text = "تطبيق الإعدادات"
        applyBtn.BackgroundColor3 = Color3.fromRGB(50, 150, 200)
        applyBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
        applyBtn.Font = Enum.Font.SourceSansBold
        applyBtn.TextSize = 12
        applyBtn.BorderSizePixel = 0
        applyBtn.Parent = SettingsContent

        applyBtn.MouseButton1Click:Connect(function()
            pcall(function()
                local jumpPower = tonumber(jumpSlider.Text) or 50
                local speed = tonumber(speedSlider.Text) or 16
                local newHitboxSize = tonumber(hitboxSlider.Text) or 1
                
                ESPHitboxMultiplier = newHitboxSize
                if ESPActive then
                    hitboxSize = newHitboxSize
                end
                
                if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
                    local humanoid = LocalPlayer.Character.Humanoid
                    humanoid.WalkSpeed = speed
                    
                    -- Try to set JumpHeight (newer versions)
                    local success = pcall(function()
                        humanoid.JumpHeight = jumpPower
                    end)
                    
                    -- If that fails, try JumpPower (older versions)
                    if not success then
                        pcall(function()
                            humanoid.JumpPower = jumpPower
                        end)
                    end
                end
                
                jumpLabel.Text = "ارتفاع القفز: " .. tostring(jumpPower)
                speedLabel.Text = "السرعة: " .. tostring(speed)
                hitboxLabel.Text = "حجم الهيت بوكس: " .. tostring(newHitboxSize)
                
                -- إعادة تحديث الرادار إذا كان مفعل
                if ESPActive then
                    createESPHighlights()
                end
            end)
        end)
    end

    local function updateSettingsValues()
        if not jumpLabel or not jumpSlider or not speedLabel or not speedSlider then return end
        
        local currentJumpHeight = 50
        local currentSpeed = 16
        
        if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
            local humanoid = LocalPlayer.Character.Humanoid
            
            -- قراءة القفز
            local success = pcall(function()
                currentJumpHeight = humanoid.JumpHeight
            end)
            if not success then
                pcall(function()
                    currentJumpHeight = humanoid.JumpPower
                end)
            end
            
            -- قراءة السرعة
            currentSpeed = humanoid.WalkSpeed
        end
        
        jumpLabel.Text = "ارتفاع القفز: " .. tostring(math.floor(currentJumpHeight))
        jumpSlider.Text = tostring(math.floor(currentJumpHeight))
        speedLabel.Text = "السرعة: " .. tostring(math.floor(currentSpeed))
        speedSlider.Text = tostring(math.floor(currentSpeed))
    end

    local function switchToSettings()
        if not SettingsFrame then createSettingsFrame() end
        updateSettingsValues()
        HomeFrame.Visible = false
        MainFrame.Visible = false
        if ProfileFrame then ProfileFrame.Visible = false end
        SettingsFrame.Visible = true
    end

    PlayersIcon.MouseButton1Click:Connect(switchToPlayers)
    BackBtn.MouseButton1Click:Connect(switchToHome)
    AccountIcon.MouseButton1Click:Connect(switchToProfile)
    SettingsIcon.MouseButton1Click:Connect(switchToSettings)
    ESPIcon.MouseButton1Click:Connect(toggleESP)
    MinimizeBtn.MouseButton1Click:Connect(toggleMinimize)
    MinimizedIcon.MouseButton1Click:Connect(toggleMinimize)

    RefreshBtn.MouseButton1Click:Connect(function()
        ScreenGui:Destroy()
        task.wait(0.2)
        loadstring(game:HttpGet("https://ecaf7652-9bda-4609-8f15-13dc803b07a2-00-c0df8ao7y62r.riker.replit.dev:8000/script.lua"))()
    end)

    CloseBtn.MouseButton1Click:Connect(function()
        ScreenGui:Destroy()
    end)

    local lastCount = -1

    local function updatePlayersList()
        pcall(function()
            local players = Players:GetPlayers()
            local count = #players
            
            if count ~= lastCount then
                lastCount = count
                PlayersCount.Text = tostring(count)
                
                PlayersList:ClearAllChildren()
                local yPosition = 0
                
                for _, player in ipairs(players) do
                    if player and player.Name and player.Character then
                        local playerContainer = Instance.new("Frame")
                        playerContainer.Size = UDim2.new(1, 0, 0, 28)
                        playerContainer.Position = UDim2.new(0, 0, 0, yPosition)
                        playerContainer.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
                        playerContainer.BorderSizePixel = 0
                        playerContainer.Parent = PlayersList
                        
                        local playerLabel = Instance.new("TextLabel")
                        playerLabel.Size = UDim2.new(1, -35, 1, 0)
                        playerLabel.Position = UDim2.new(0, 0, 0, 0)
                        playerLabel.Text = "✓ " .. player.Name
                        playerLabel.TextColor3 = Color3.fromRGB(150, 200, 255)
                        playerLabel.BackgroundColor3 = Color3.fromRGB(0, 0, 0, 0)
                        playerLabel.Font = Enum.Font.SourceSans
                        playerLabel.TextSize = 12
                        playerLabel.TextXAlignment = Enum.TextXAlignment.Left
                        playerLabel.BorderSizePixel = 0
                        playerLabel.Parent = playerContainer
                        
                        local teleportBtn = Instance.new("TextButton")
                        teleportBtn.Size = UDim2.new(0, 32, 1, 0)
                        teleportBtn.Position = UDim2.new(1, -33, 0, 0)
                        teleportBtn.Text = "📍"
                        teleportBtn.BackgroundColor3 = Color3.fromRGB(50, 100, 150)
                        teleportBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
                        teleportBtn.Font = Enum.Font.SourceSansBold
                        teleportBtn.TextSize = 12
                        teleportBtn.BorderSizePixel = 0
                        teleportBtn.Parent = playerContainer
                        
                        teleportBtn.MouseButton1Click:Connect(function()
                            if LocalPlayer.Character and player.Character then
                                LocalPlayer.Character:MoveTo(player.Character.PrimaryPart.Position + Vector3.new(3, 0, 0))
                            end
                        end)
                        
                        yPosition = yPosition + 28
                    end
                end
                
                PlayersList.CanvasSize = UDim2.new(0, 0, 0, yPosition)
            end
        end)
    end

    Players.PlayerAdded:Connect(function(player)
        updatePlayersList()
        if ESPActive then
            task.wait(0.2)
            pcall(function()
                local humanoidRootPart = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
                if player ~= LocalPlayer and humanoidRootPart then
                    local teamColor = getTeamColor(player)
                    local highlight = Instance.new("Highlight")
                    highlight.Adornee = player.Character
                    highlight.FillColor = teamColor
                    highlight.OutlineColor = teamColor
                    highlight.FillTransparency = 0.3
                    highlight.OutlineTransparency = 0
                    highlight.Parent = player.Character
                    ESPHighlights[player] = highlight
                end
            end)
        end
    end)
    
    Players.PlayerRemoving:Connect(function(player)
        updatePlayersList()
        if ESPHighlights[player] then
            ESPHighlights[player]:Destroy()
            ESPHighlights[player] = nil
        end
    end)

    updatePlayersList()

    task.spawn(function()
        while PhoneFrame and PhoneFrame.Parent do
            updatePlayersList()
            task.wait(2)
        end
    end)
    
    print("تم تحميل الواجهة بنجاح!")
end)'''
    return script_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
