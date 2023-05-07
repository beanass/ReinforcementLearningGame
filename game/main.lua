--[[
    GD50
    Super Mario Bros. Remake

    Author: Colton Ogden
    cogden@cs50.harvard.edu
    
    A classic platformer in the style of Super Mario Bros., using a free
    art pack. Super Mario Bros. was instrumental in the resurgence of video
    games in the mid-80s, following the infamous crash shortly after the
    Atari age of the late 70s. The goal is to navigate various levels from
    a side perspective, where jumping onto enemies inflicts damage and
    jumping up into blocks typically breaks them or reveals a powerup.

    Art pack:
    https://opengameart.org/content/kenney-16x16

    Music:
    https://freesound.org/people/Sirkoto51/sounds/393818/
]]

love.graphics.setDefaultFilter('nearest', 'nearest')
require 'src/Dependencies'

local socket = require("socket")
local json = require("lib/JSON")

local server = socket.tcp()
server:bind("127.0.0.1", 8080)
server:listen(1)
server:settimeout(0)

local client = nil

local function sendGameState(client, gameState)
    local jsonGameState = json.encode(gameState)
    client:send(jsonGameState .. "\n")
end

function love.load()
    love.graphics.setFont(gFonts['medium'])
    love.window.setTitle('Super 50 Bros.')

    math.randomseed(os.time())
    
    push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, {
        fullscreen = false,
        vsync = true,
        resizable = true,
        canvas = false
    })

    gStateMachine = StateMachine {
        ['start'] = function() return StartState() end,
        ['play'] = function() return PlayState() end
    }
    gStateMachine:change('start')

    gSounds['music']:setLooping(true)
    gSounds['music']:setVolume(0.5)
    gSounds['music']:play()

    love.keyboard.keysPressed = {}
end

function love.resize(w, h)
    push:resize(w, h)
end

function love.keypressed(key)
    if key == 'escape' then
        love.event.quit()
    end

    love.keyboard.keysPressed[key] = true
end

function love.keyboard.wasPressed(key)
    return love.keyboard.keysPressed[key]
end

function love.update(dt)
    if not client then
        client = server:accept()
    end

    gStateMachine:update(dt)

    --stateJson = json:encode(gStateMachine.name)
    if gStateMachine.current.level then 
        gameState = getGameState(gStateMachine)
        levelJson = json:encode(gameState)
        print(string.len(levelJson))
    end

    if client then
        client:settimeout(0)
        if levelJson then
            client:send(levelJson .. "\n")
        end
    end

    love.keyboard.keysPressed = {}
end

function love.draw()
    push:start()
    gStateMachine:render()
    push:finish()
end

function love.quit()
    server:close()
end

function getGameState(gStateMachine)
    gameState = {}

    newPlayer = shallowcopy(gStateMachine.current.player)
    newPlayer.level = nil
    newPlayer.map = nil
    newPlayer.stateMachine = nil
    gameState.player = newPlayer

    entityTable = {}
    for k, entity in pairs(gStateMachine.current.level.entities) do
        newEntity = shallowcopy(entity)
        newEntity.level = nil
        newEntity.map = nil
        newEntity.stateMachine = nil
        table.insert(entityTable, newEntity)
    end
    gameState.entities = entityTable

    objectTable = {}
    for k, object in pairs(gStateMachine.current.level.objects) do
        newObject = shallowcopy(object)
        newObject.level = nil
        newObject.map = nil
        newObject.stateMachine = nil
        newObject.onCollide = nil
        newObject.onConsume = nil
        table.insert(objectTable, newObject)
    end
    gameState.objects = objectTable

    return gameState
end

function shallowcopy(orig)
    local orig_type = type(orig)
    local copy
    if orig_type == 'table' then
        copy = {}
        for orig_key, orig_value in pairs(orig) do
            copy[orig_key] = orig_value
        end
    else -- number, string, boolean, etc
        copy = orig
    end
    return copy
end