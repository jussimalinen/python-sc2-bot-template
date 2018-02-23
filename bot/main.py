import json
from pathlib import Path

import sc2
from sc2.constants import *

class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    async def on_step(self, iteration):
        await self.build_supply_if_needed()
        await self.build_workers()
        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")

    async def build_supply_if_needed(self):
        cc = self.units(UnitTypeId.COMMANDCENTER)
        if self.supply_left < (2 if self.units(BARRACKS).amount < 3 else 4):
            if self.can_afford(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) < 2:
                await self.build(UnitTypeId.SUPPLYDEPOT, near=cc[-1].position.towards(self.game_info.map_center, 5))

    async def build_workers(self):
        for cc in self.units(UnitTypeId.COMMANDCENTER).ready.noqueue:
            if self.can_afford(UnitTypeId.SCV):
                await self.do(cc.train(UnitTypeId.SCV))