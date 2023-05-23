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

    if client then
        --keys = json:decode(client:recv()) 
        
    end

    gStateMachine:update(dt)

    --stateJson = json:encode(gStateMachine.name)
    if gStateMachine.current.level then 
        gameState = getGameState(gStateMachine)
        levelJson = json:encode(gameState)
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
    player = {}
    player.x = newPlayer.x
    player.y = newPlayer.y
    player.dx = newPlayer.dx
    player.dy = newPlayer.dy
    player.score = newPlayer.score
    player.hasKey = newPlayer.hasKey
    gameState.player = player
    playerX = newPlayer.x

    entityTable = {}
    for k, entity in pairs(gStateMachine.current.level.entities) do
        newEntity = shallowcopy(entity)
        ent = {}
        ent.x = newEntity.x
        ent.y = newEntity.y
        ent.dx = newEntity.dx
        ent.dy = newEntity.dy
        table.insert(entityTable, ent)
    end
    gameState.entities = entityTable

    objectTable = {}
    for k, object in pairs(gStateMachine.current.level.objects) do
        if object.texture == 'bushes' then

        else
            newObject = shallowcopy(object)
            obj = {}
            obj.x = newObject.x
            obj.y = newObject.y
            obj.texture = newObject.texture
            table.insert(objectTable, obj)
        end
    end
    gameState.objects = objectTable

    tileMatrix = {}
    for y = 0, VIRTUAL_HEIGHT, TILE_SIZE do
        tileRow = {}
        for x = playerX - (4 * TILE_SIZE), playerX + (16 * TILE_SIZE), TILE_SIZE do
            tile = gStateMachine.current.level.tileMap:pointToTile(x, y)
            if tile then
                if tile.id == TILE_ID_EMPTY then
                    table.insert(tileRow, 0)
                else
                    table.insert(tileRow, 1)
                end
            end
        end
        table.insert(tileMatrix, tileRow)
    end
    table.insert(tileMatrix, TILE_SIZE)
    gameState.tileMatrix = tileMatrix

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