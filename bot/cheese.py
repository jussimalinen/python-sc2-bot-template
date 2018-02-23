import json
from pathlib import Path

import sc2
from sc2.constants import *

class CheeseBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):
        self.STEPS = [
            [14, self.build_depot],
            [15, self.build_barracks],
            [15, self.build_refinery],
            [16, self.build_refinery],
            [20, self.build_barracks_tech_lab],
            [20, self.build_ghost_academy],
            [20, self.build_orbital_command],
            [20, self.build_depot],
            [20, self.build_ghost],
            [20, self.build_factory],
            [20, self.build_ghost],
            [24, self.build_depot],
            [26, self.build_factory_reactor],
            [26, self.build_depot],
            [27, self.build_cyclone],
            [27, self.build_cyclone],
            [27, self.attaaaaack],
            [999, self.build_depot]
        ]
        self.refineries = [];

    async def build_refinery(self):
        cc = self.units(UnitTypeId.COMMANDCENTER)[0]
        if self.can_afford(UnitTypeId.REFINERY):
            vgs = self.state.vespene_geyser.closer_than(20.0, cc)
            for vg in vgs:
                if self.units(UnitTypeId.REFINERY).closer_than(1.0, vg).exists:
                    break
                worker = self.select_build_worker(vg.position)
                if worker is None:
                    break
                if vg.tag in self.refineries:
                    break
                if vg.name != 'VespeneGeyser':
                    break
                self.refineries.append(vg.tag)
                await self.do(worker.build(UnitTypeId.REFINERY, vg))
                return True


    async def build_barracks_tech_lab(self):
        ready_raxes = self.units(UnitTypeId.BARRACKS).ready
        if ready_raxes.amount > 0 and self.can_afford(UnitTypeId.BARRACKSTECHLAB):
            await self.do(ready_raxes[0].train(UnitTypeId.BARRACKSTECHLAB))
            return True


    async def build_ghost_academy(self):
        return

    async def build_orbital_command(self):
        return

    async def build_ghost(self):
        return

    async def build_factory(self):
        return

    async def build_factory_reactor(self):
        return

    async def build_cyclone(self):
        return

    async def attaaaaack(self):
        return

    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")
        worker_count = self.workers.amount
        next_step_count = self.STEPS[0][0]
        if worker_count >= next_step_count:
            executed = await self.STEPS[0][1]()
            if executed:
                print("EXECUTED STEP {} {}".format(next_step_count, self.STEPS[0][1].__name__))
                self.STEPS.pop(0)
                return executed
        else:
            await self.build_workers()

    async def build_depot(self):
        cc = self.units(UnitTypeId.COMMANDCENTER)
        if self.can_afford(UnitTypeId.SUPPLYDEPOT):
            await self.build(UnitTypeId.SUPPLYDEPOT, near=cc[-1].position.towards(self.game_info.map_center, 5))
            return True

    async def build_barracks(self):
        cc = self.units(UnitTypeId.COMMANDCENTER)
        if self.can_afford(UnitTypeId.BARRACKS) and self.units(UnitTypeId.SUPPLYDEPOT).ready.amount > 0:
            await self.build(UnitTypeId.BARRACKS, near=cc[-1].position.towards(self.game_info.map_center, 5))
            return True

    async def build_workers(self):
        for cc in self.units(UnitTypeId.COMMANDCENTER).ready.noqueue:
            if self.can_afford(UnitTypeId.SCV):
                print("Building worker, current count {}".format(self.workers.amount))
                await self.do(cc.train(UnitTypeId.SCV))
                return True

