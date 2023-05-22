--[[
    GD50
    Super Mario Bros. Remake

    -- LevelMaker Class --

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

LevelMaker = Class{}

function LevelMaker.generate(width, height)
    local tiles = {}
    local entities = {}
    local objects = {}
    local keyX = math.random(2, math.floor(width/2))
    local lockX = math.random(math.floor(width/2), width - 10)
    local lockColor = math.random(1, 4)

    local tileID = TILE_ID_GROUND
    
    -- whether we should draw our tiles with toppers
    local topper = true
    local tileset = math.random(20)
    local topperset = math.random(20)

    -- insert blank tables into tiles for later access
    for x = 1, height do
        table.insert(tiles, {})
    end

    -- column by column generation instead of row; sometimes better for platformers
    for x = 1, width do
        local tileID = TILE_ID_EMPTY
        
        -- lay out the empty space
        for y = 1, 6 do
            table.insert(tiles[y],
                Tile(x, y, tileID, nil, tileset, topperset))
        end

        -- chance to just be emptiness
        if math.random(7) == 1 and x ~= keyX and x ~= lockX then
            for y = 7, height do
                table.insert(tiles[y],
                    Tile(x, y, tileID, nil, tileset, topperset))
            end
        else
            tileID = TILE_ID_GROUND

            -- height at which we would spawn a potential jump block
            local blockHeight = 4
            local highestBlock = 7

            for y = 7, height do
                table.insert(tiles[y],
                    Tile(x, y, tileID, y == 7 and topper or nil, tileset, topperset))
            end

            -- chance to generate a pillar
            if math.random(8) == 1 then
                blockHeight = 2
                highestBlock = 5
                
                -- chance to generate bush on pillar
                if math.random(8) == 1 then
                    table.insert(objects,
                        GameObject {
                            texture = 'bushes',
                            x = (x - 1) * TILE_SIZE,
                            y = (4 - 1) * TILE_SIZE,
                            width = 16,
                            height = 16,
                            
                            -- select random frame from bush_ids whitelist, then random row for variance
                            frame = BUSH_IDS[math.random(#BUSH_IDS)] + (math.random(4) - 1) * 7,
                            collidable = false
                        }
                    )
                
                end
                
                -- pillar tiles
                tiles[5][x] = Tile(x, 5, tileID, topper, tileset, topperset)
                tiles[6][x] = Tile(x, 6, tileID, nil, tileset, topperset)
                tiles[7][x].topper = nil
            
            -- chance to generate bushes
            elseif math.random(8) == 1 then
                table.insert(objects,
                    GameObject {
                        texture = 'bushes',
                        x = (x - 1) * TILE_SIZE,
                        y = (6 - 1) * TILE_SIZE,
                        width = 16,
                        height = 16,
                        frame = BUSH_IDS[math.random(#BUSH_IDS)] + (math.random(4) - 1) * 7,
                        collidable = false
                    }
                )
            end

            if x == keyX then
                table.insert(objects,
                    GameObject {
                        texture = 'keys-and-locks',
                        x = (x - 1) * TILE_SIZE,
                        y = (highestBlock - 2) * TILE_SIZE,
                        width = 16,
                        height = 16,
                        frame = KEYS[lockColor],
                        collidable = true,
                        consumable = true,
                        solid = false,
                        onConsume = function(player, object)
                            gSounds['pickup']:play()
                            player.keyx = player.x-player.width
                            player.keyy = player.y+16
                            player.hasKey = true
                            player.key = KEYS[lockColor]
                            object.collidable = false
                            object.consumable = false
                            return true
                        end,
                        key = true
                    }
                )
            end

            if x == lockX then
                table.insert(objects,
                    GameObject {
                        texture = 'keys-and-locks',
                        x = (x - 1) * TILE_SIZE,
                        y = (highestBlock - 2) * TILE_SIZE,
                        width = 16,
                        height = 16,
                        frame = LOCKS[lockColor],
                        collidable = true,
                        consumable = true,
                        solid = false,
                        onConsume = function(player, object)
                            if player.hasKey then
                                object.collidable = false
                                object.consumable = false
                                player.consumingKey = true
                                local goal = player.direction == 'left' and object.x or object.x+object.width
                                local timer = Timer.tween(0.5, {
                                    [player] = {keyx = goal, keyy = object.y}
                                }):finish(function()
                                    gSounds['pickup']:play()
                                    player.hasKey = false
                                    player.consumingKey = false
                                    for x = width, 1, -1 do
                                        for y = 1, height do
                                            if tiles[y][x-1].id == TILE_ID_GROUND then
                                                spawnFlagpole(width, objects, x-1, y-1)
                                                return
                                            end
                                        end
                                    end
                                end)
                                return true
                            end
                            return false
                        end
                    }
                )
            end

            -- chance to spawn a block
            if math.random(10) == 1 then
                table.insert(objects,

                    -- jump block
                    GameObject {
                        texture = 'jump-blocks',
                        x = (x - 1) * TILE_SIZE,
                        y = (blockHeight - 1) * TILE_SIZE,
                        width = 16,
                        height = 16,

                        -- make it a random variant
                        frame = math.random(#JUMP_BLOCKS),
                        collidable = true,
                        hit = false,
                        solid = true,

                        -- collision function takes itself
                        onCollide = function(obj)

                            -- spawn a gem if we haven't already hit the block
                            if not obj.hit then

                                -- chance to spawn gem, not guaranteed
                                if math.random(5) == 1 then

                                    -- maintain reference so we can set it to nil
                                    local gem = GameObject {
                                        texture = 'gems',
                                        x = (x - 1) * TILE_SIZE,
                                        y = (blockHeight - 1) * TILE_SIZE - 4,
                                        width = 16,
                                        height = 16,
                                        frame = math.random(#GEMS),
                                        collidable = true,
                                        consumable = true,
                                        solid = false,

                                        -- gem has its own function to add to the player's score
                                        onConsume = function(player, object)
                                            gSounds['pickup']:play()
                                            player.score = player.score + 100
                                            return true
                                        end
                                    }
                                    
                                    -- make the gem move up from the block and play a sound
                                    Timer.tween(0.1, {
                                        [gem] = {y = (blockHeight - 2) * TILE_SIZE}
                                    })
                                    gSounds['powerup-reveal']:play()

                                    table.insert(objects, gem)
                                end

                                obj.hit = true
                            end

                            gSounds['empty-block']:play()
                        end
                    }
                )
            end
        end
    end

    local map = TileMap(width, height)
    map.tiles = tiles
    
    return GameLevel(entities, objects, map)
end

function spawnFlagpole(width, objects, x, y)
    local poleColor = math.random(6)
    local poleBottom = GameObject {
        texture = 'flags',
        x = (x - 1) * TILE_SIZE,
        y = (y - 1) * TILE_SIZE,
        width = 16,
        height = 16,
        frame = poleColor+18,
        collidable = false,
        consumable = true,
        solid = false,
        onConsume = function(player, object)
            gSounds['powerup-reveal']:play()
            gStateMachine:change('play', {
                score = player.score,
                levelwidth = math.floor(width*1.25)
            })
        end
    }
    table.insert(objects, poleBottom)

    local poleHeight = math.random(3)
    for i = 1, poleHeight do
        local poleMid = GameObject {
            texture = 'flags',
            x = (x - 1) * TILE_SIZE,
            y = (y - 1 - i) * TILE_SIZE,
            width = 16,
            height = 16,
            frame = poleColor+9,
            collidable = false,
            consumable = true,
            solid = false,
            onConsume = function(player, object)
                gSounds['powerup-reveal']:play()
                gStateMachine:change('play', {
                    score = player.score,
                    levelwidth = math.floor(width*1.25)
                })
            end
        }
        table.insert(objects, poleMid)
    end

    local poleTop = GameObject {
        texture = 'flags',
        x = (x - 1) * TILE_SIZE,
        y = (y - (2 + poleHeight)) * TILE_SIZE,
        width = 16,
        height = 16,
        frame = poleColor,
        collidable = false,
        consumable = true,
        solid = false,
        onConsume = function(player, object)
            gSounds['powerup-reveal']:play()
            gStateMachine:change('play', {
                score = player.score,
                levelwidth = math.floor(width*1.25)
            })
        end
    }
    table.insert(objects, poleTop)

    local flagCount = math.random(3)
    for i = 1, flagCount do
        local flagColor = (math.random(4)-1)*9+7
        local flag = GameObject {
            texture = 'flags',
            x = (x - 1) * TILE_SIZE + 8,
            y = (y - (3 + poleHeight) + i) * TILE_SIZE,
            width = 16,
            height = 16,
            frame = flagColor,
            collidable = false,
            consumable = false,
            solid = false,
            animation = Animation {
                frames = {flagColor, flagColor+1},
                interval = 0.3
            }
        }
        table.insert(objects, flag)
    end
end