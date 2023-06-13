# Report Steam

## Report Title:

Filippo Fiorenza 205 194
Patrick Sandmann
Dennis Erbe

Semester: SS2023, Repo: Steam, Course ID: 262058, Course name: Datenbanken 1

## Introduction:

### Access Patterns

1. As a user, I would like to be able to create an account for myself
2. As a game developer, I want to be able to provide the updated version of my game software
3. As an admin, I should be able to delete the account of players who have repeatedly attracted attention by cheating in multiplayer games.
4. As a friend of another user, I would like to see what games he has in his library.
5. As a user, I would like to put the games I want on my wishlist
6. As a game developer, I would like to update the price of my offered games

## Data Model:

### Entity-Relationship Diagram

```mermaid
erDiagram
    GAME o{--o{ LIBRARY : has
        GAME {
        id int
        name string
        genre string
        publisher string
        developer string
        franchise string
        price int
        size int
        rating int
        USK int
        releaseDate DateTime
        supportedPlatforms string
        supportedLanguages string
        description string
    }
    LIBRARY {
        id int
        game game
        timePlayed DateTime
        lastPlayed DateTime
        CloudSaveStatus boolean
        gameID int
    }
    GUIDE }o--|| GAME : has
        GUIDE {
            id int
            name string
            text string
            picture PNG
            userID int
    }
    WISHLIST }o--o{ GAME : listed
        WISHLIST {
            userID int
            gameID int            
        }
    ACHIEVEMENT }o--|| GAME : "has"
        ACHIEVEMENT {
            id int
            name string
            description string
            gameID int
        }
    REVIEW }o--|| GAME : has    
        REVIEW {
            id int
            heading string
            text string
            rating int
            userID int
        }

    GUIDE }o--|| USER : has
    WISHLIST ||--|| USER : has
    %%ACHIEVEMENT }o--o{ USER : "achieved"
    REVIEW }o--|| USER : has    
    INVENTORY ||--|| USER : has
        INVENTORY {
            userID int
            itemID int
        }

    USER ||--|| LIBRARY : "has"
        USER {
            id int
            library int
            username string
            addres string
            firstname string
            lastname string
            birthday DateTime
            VAC boolean
            inventory int
            level int
        }
    USER }o--o{ USER : "friends with"    
    ITEM }o--o{ INVENTORY : "assigned to"

    ACHIVED_BY }o--|| USER : has
        ACHIVED_BY {
            userID int
            achievementID int
            timestamp DateTime
        }
    ACHIVED_BY }o--|| ACHIEVEMENT: has
    ITEM {
        itemID int
        name string
        description string
    }
```

## Tooling:


## Lessons Learned:
