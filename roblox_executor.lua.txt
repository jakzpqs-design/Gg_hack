local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local HttpService = game:GetService("HttpService")
local CoreGui = game:GetService("CoreGui")

local BACKEND_URL = "https://ecaf7652-9bda-4609-8f15-13dc803b07a2-00-c0df8ao7y62r.riker.replit.dev"

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "ToolFinderGUI"
ScreenGui.Parent = CoreGui
ScreenGui.ResetOnSpawn = false

local MainFrame = Instance.new("Frame")
MainFrame.Size = UDim2.new(0, 300, 0, 400)
MainFrame.Position = UDim2.new(0.5, -150, 0.5, -200)
MainFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
MainFrame.Parent = ScreenGui

local frameCorner = Instance.new("UICorner")
frameCorner.CornerRadius = UDim.new(0, 6)
frameCorner.Parent = MainFrame

local Title = Instance.new("TextLabel")
Title.Size = UDim2.new(1, 0, 0, 40)
Title.Text = "🔍 أدواتك متصلة بـ Cloud"
Title.TextColor3 = Color3.fromRGB(255, 255, 255)
Title.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
Title.Font = Enum.Font.SourceSansBold
Title.TextSize = 16
Title.Parent = MainFrame

local SaveBtn = Instance.new("TextButton")
SaveBtn.Size = UDim2.new(0.9, 0, 0, 40)
SaveBtn.Position = UDim2.new(0.05, 0, 0, 50)
SaveBtn.Text = "☁️ حفظ الأدوات في السحابة"
SaveBtn.BackgroundColor3 = Color3.fromRGB(0, 150, 200)
SaveBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
SaveBtn.Font = Enum.Font.SourceSansBold
SaveBtn.TextSize = 14
SaveBtn.Parent = MainFrame

local LoadBtn = Instance.new("TextButton")
LoadBtn.Size = UDim2.new(0.9, 0, 0, 40)
LoadBtn.Position = UDim2.new(0.05, 0, 0, 100)
LoadBtn.Text = "📥 استرجاع الأدوات من السحابة"
LoadBtn.BackgroundColor3 = Color3.fromRGB(0, 120, 180)
LoadBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
LoadBtn.Font = Enum.Font.SourceSansBold
LoadBtn.TextSize = 14
LoadBtn.Parent = MainFrame

local StatusBox = Instance.new("TextBox")
StatusBox.Size = UDim2.new(0.9, 0, 0, 200)
StatusBox.Position = UDim2.new(0.05, 0, 0, 150)
StatusBox.Text = "✅ البرنامج جاهز!\n\nاضغط على الأزرار أعلاه"
StatusBox.TextColor3 = Color3.fromRGB(100, 255, 100)
StatusBox.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
StatusBox.TextScaled = true
StatusBox.MultiLine = true
StatusBox.Font = Enum.Font.Code
StatusBox.TextSize = 12
StatusBox.Parent = MainFrame

local function updateStatus(message)
    StatusBox.Text = message
end

SaveBtn.MouseButton1Click:Connect(function()
    updateStatus("⏳ جاري الحفظ...")
    
    local tools = {}
    if LocalPlayer.Character then
        for _, tool in ipairs(LocalPlayer.Character:GetChildren()) do
            if tool:IsA("Tool") then
                table.insert(tools, tool.Name)
            end
        end
    end
    
    local payload = {
        player = LocalPlayer.Name,
        tools = tools
    }
    
    pcall(function()
        local response = HttpService:PostAsync(
            BACKEND_URL .. "/save-tools",
            HttpService:JSONEncode(payload),
            Enum.HttpContentType.ApplicationJson
        )
        
        local decoded = HttpService:JSONDecode(response)
        if decoded.success then
            updateStatus("✅ تم الحفظ بنجاح!\n\nأدواتك المحفوظة:\n• " .. table.concat(tools, "\n• "))
        else
            updateStatus("❌ خطأ: " .. (decoded.error or "حدث خطأ"))
        end
    end)
end)

LoadBtn.MouseButton1Click:Connect(function()
    updateStatus("⏳ جاري التحميل...")
    
    pcall(function()
        local response = HttpService:GetAsync(
            BACKEND_URL .. "/get-tools/" .. LocalPlayer.Name
        )
        
        local decoded = HttpService:JSONDecode(response)
        if decoded.success then
            local tools = decoded.tools
            if #tools > 0 then
                updateStatus("✅ تم التحميل بنجاح!\n\nالأدوات المُسترجعة:\n• " .. table.concat(tools, "\n• "))
            else
                updateStatus("⚠️ لا توجد أدوات محفوظة")
            end
        else
            updateStatus("❌ لم توجد أدوات محفوظة")
        end
    end)
end)
