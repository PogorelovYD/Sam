import random
import heapq
import itertools
from dataclasses import dataclass
 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
# =========================
# ЭТАП 1. BANDWIDTH
# =========================
 
def calculate_bandwidth(nodes, fanout, packet_size_bytes, interval):
    """
    Расчёт пропускной способности Gossip-протокола.
 
    nodes - количество узлов
    fanout - сколько соседей выбирает каждый узел
    packet_size_bytes - размер одного сообщения
    interval - интервал gossip-рассылки в секундах
 
    Возвращает bandwidth в бит/сек.
    """
    messages_per_second = nodes * fanout / interval
    bandwidth_bps = messages_per_second * packet_size_bytes * 8
    return bandwidth_bps
 
def plot_bandwidth():
    nodes = 100
    fanout = 3
    packet_size_bytes = 256
 
    intervals = np.linspace(0.1, 2.0, 20)
    bandwidth_values = [
        calculate_bandwidth(nodes, fanout, packet_size_bytes, interval)
        for interval in intervals
    ]
 
    plt.figure(figsize=(8, 5))
    plt.plot(intervals, bandwidth_values, marker="o")
    plt.title("Зависимость Bandwidth от Gossip Interval")
    plt.xlabel("Gossip Interval, сек")
    plt.ylabel("Bandwidth, бит/сек")
    plt.grid(True)
    plt.savefig("bandwidth_vs_interval.png")
    plt.show()
 
# =========================
# БАЗОВЫЙ СИМУЛЯТОР
# =========================
 
@dataclass
class SimulationResult:
    protocol: str
    first_detection_time: float
    full_convergence_time: float
    total_messages: int
    latency_max: float
 
class BaseSimulator:
    def __init__(
        self,
        nodes=100,
        failures_percent=5,
        interval=0.2,
        fanout=3,
        packet_loss=0.05,
        latency_min=0.0,
        latency_max=0.5,
        max_time=120,
        seed=None
    ):
        self.nodes = nodes
        self.failures_percent = failures_percent
        self.interval = interval
        self.fanout = fanout
        self.packet_loss = packet_loss
        self.latency_min = latency_min
        self.latency_max = latency_max
        self.max_time = max_time
 
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
 
        self.all_nodes = list(range(nodes))
 
        failed_count = max(1, int(nodes * failures_percent / 100))
        self.failed_nodes = set(random.sample(self.all_nodes, failed_count))
        self.alive_nodes = [node for node in self.all_nodes if node not in self.failed_nodes]
 
        # knowledge[node] — какие отказавшие узлы известны данному узлу
        self.knowledge = {
            node: set()
            for node in self.alive_nodes
        }
 
        self.current_time = 0.0
        self.total_messages = 0
        self.first_detection_time = None
 
        self.event_queue = []
        self.event_counter = itertools.count()
 
    def is_converged(self):
        """
        Полная конвергенция наступает тогда,
        когда все живые узлы знают обо всех отказавших узлах.
        """
        for node in self.alive_nodes:
            if self.knowledge[node] != self.failed_nodes:
                return False
        return True
 
    def send_message(self, receiver, data, current_time):
        """
        Отправка сообщения с учётом потери пакета и задержки доставки.
        """
        self.total_messages += 1
 
        # имитация потери пакета
        if random.random() < self.packet_loss:
            return
 
        latency = random.uniform(self.latency_min, self.latency_max)
        delivery_time = current_time + latency
 
        event_id = next(self.event_counter)
 
        heapq.heappush(
            self.event_queue,
            (delivery_time, event_id, receiver, set(data))
        )
 
    def process_events(self, current_time):
        """
        Обработка сообщений, которые уже дошли до получателей.
        """
        while self.event_queue and self.event_queue[0][0] <= current_time:
            delivery_time, event_id, receiver, data = heapq.heappop(self.event_queue)
 
            if receiver not in self.knowledge:
                continue
 
            before = len(self.knowledge[receiver])
            self.knowledge[receiver].update(data)
            after = len(self.knowledge[receiver])
 
            if before == 0 and after > 0 and self.first_detection_time is None:
                self.first_detection_time = delivery_time
 
    def run(self):
        """
        Общий цикл симуляции.
        """
        time_points = np.arange(0, self.max_time + self.interval, self.interval)
 
        for t in time_points:
            self.current_time = float(t)
 
            self.process_events(self.current_time)
 
            if self.is_converged():
                return SimulationResult(
                    protocol=self.__class__.__name__,
                    first_detection_time=self.first_detection_time if self.first_detection_time is not None else self.max_time,
                    full_convergence_time=self.current_time,
                    total_messages=self.total_messages,
                    latency_max=self.latency_max
                )
 
            self.step()
 
            self.process_events(self.current_time)
 
            if self.is_converged():
                return SimulationResult(
                    protocol=self.__class__.__name__,
                    first_detection_time=self.first_detection_time if self.first_detection_time is not None else self.max_time,
                    full_convergence_time=self.current_time,
                    total_messages=self.total_messages,
                    latency_max=self.latency_max
                )
 
        return SimulationResult(
            protocol=self.__class__.__name__,
            first_detection_time=self.first_detection_time if self.first_detection_time is not None else self.max_time,
            full_convergence_time=self.max_time,
            total_messages=self.total_messages,
            latency_max=self.latency_max
        )
 
    def step(self):
        raise NotImplementedError
 
# =========================
# SERF / GOSSIP
# =========================
 
class SerfSimulator(BaseSimulator):
    """
    Gossip-подход.
    Каждый живой узел:
    1. случайно проверяет один узел;
    2. распространяет известную информацию fanout случайным соседям.
    """
 
    def step(self):
        for node in self.alive_nodes:
            # случайная проверка одного узла
            target = random.choice([n for n in self.all_nodes if n != node])
 
            if target in self.failed_nodes:
                self.send_message(
                    receiver=node,
                    data={target},
                    current_time=self.current_time
                )
            else:
                self.total_messages += 1
 
            # gossip-рассылка известной информации
            possible_neighbors = [n for n in self.alive_nodes if n != node]
 
            if not possible_neighbors:
                continue
 
            neighbors = random.sample(
                possible_neighbors,
                min(self.fanout, len(possible_neighbors))
            )
 
            for neighbor in neighbors:
                self.send_message(
                    receiver=neighbor,
                    data=self.knowledge[node],
                    current_time=self.current_time
                )
 
# =========================
# HEARTBEAT FULL-MESH
# =========================
 
class HeartbeatSimulator(BaseSimulator):
    """
    Full-mesh heartbeat.
    Каждый живой узел проверяет все остальные узлы.
    Быстро, но создаёт большой трафик.
    """
 
    def step(self):
        for node in self.alive_nodes:
            for target in self.all_nodes:
                if target == node:
                    continue
 
                if target in self.failed_nodes:
                    self.send_message(
                        receiver=node,
                        data={target},
                        current_time=self.current_time
                    )
                else:
                    self.total_messages += 1
 
# =========================
# PING RANDOM PROBE
# =========================
 
class PingSimulator(BaseSimulator):
    """
    Random Ping.
    Каждый живой узел проверяет одного случайного соседа.
    Трафик маленький, но сходимость медленная.
    """
 
    def step(self):
        for node in self.alive_nodes:
            target = random.choice([n for n in self.all_nodes if n != node])
 
            if target in self.failed_nodes:
                self.send_message(
                    receiver=node,
                    data={target},
                    current_time=self.current_time
                )
            else:
                self.total_messages += 1
 
# =========================
# ЭТАП 3. СРАВНЕНИЕ ПРОТОКОЛОВ
# =========================
 
def run_comparison(trials=20):
    results = []
 
    simulators = [
        SerfSimulator,
        HeartbeatSimulator,
        PingSimulator
    ]
 
    for simulator_class in simulators:
        for i in range(trials):
            simulator = simulator_class(
                nodes=100,
                failures_percent=5,
                interval=0.2,
                fanout=3,
                packet_loss=0.05,
                latency_min=0.0,
                latency_max=0.5,
                max_time=120,
                seed=i
            )
 
            result = simulator.run()
            results.append(result)
 
    df = pd.DataFrame([r.__dict__ for r in results])
    df.to_csv("comparison_results.csv", index=False)
 
    print("\n=== Сравнительная таблица ===")
    print(df.groupby("protocol")[[
        "first_detection_time",
        "full_convergence_time",
        "total_messages"
    ]].mean())
 
    return df
 
def plot_comparison(df):
    metrics = [
        "first_detection_time",
        "full_convergence_time",
        "total_messages"
    ]
 
    titles = [
        "Время первого обнаружения сбоя",
        "Время полной конвергенции",
        "Суммарное количество сообщений"
    ]
 
    filenames = [
        "boxplot_first_detection.png",
        "boxplot_full_convergence.png",
        "boxplot_total_messages.png"
    ]
 
    for metric, title, filename in zip(metrics, titles, filenames):
        plt.figure(figsize=(8, 5))
        df.boxplot(column=metric, by="protocol")
        plt.title(title)
        plt.suptitle("")
        plt.xlabel("Протокол")
        plt.ylabel(metric)
        plt.grid(True)
        plt.savefig(filename)
        plt.show()
 
# =========================
# ИНДИВИДУАЛЬНОЕ ЗАДАНИЕ ВАРИАНТА 16
# ВЛИЯНИЕ LATENCY 0-500 мс
# =========================
 
def run_latency_experiment(trials=15):
    latency_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    results = []
 
    for latency in latency_values:
        for i in range(trials):
            simulator = SerfSimulator(
                nodes=100,
                failures_percent=5,
                interval=0.2,
                fanout=3,
                packet_loss=0.05,
                latency_min=0.0,
                latency_max=latency,
                max_time=120,
                seed=i
            )
 
            result = simulator.run()
            results.append(result)
 
    df = pd.DataFrame([r.__dict__ for r in results])
    df.to_csv("latency_experiment_results.csv", index=False)
 
    print("\n=== Влияние latency на Gossip / Serf ===")
    print(df.groupby("latency_max")[[
        "first_detection_time",
        "full_convergence_time",
        "total_messages"
    ]].mean())
 
    return df
 
def plot_latency_experiment(df):
    grouped = df.groupby("latency_max").mean(numeric_only=True).reset_index()
 
    plt.figure(figsize=(8, 5))
    plt.plot(grouped["latency_max"], grouped["full_convergence_time"], marker="o")
    plt.title("Влияние задержки на время полной конвергенции Gossip")
    plt.xlabel("Максимальная задержка доставки, сек")
    plt.ylabel("Время полной конвергенции, сек")
    plt.grid(True)
    plt.savefig("latency_vs_convergence.png")
    plt.show()
 
    plt.figure(figsize=(8, 5))
    plt.plot(grouped["latency_max"], grouped["first_detection_time"], marker="o")
    plt.title("Влияние задержки на время первого обнаружения сбоя")
    plt.xlabel("Максимальная задержка доставки, сек")
    plt.ylabel("Время первого обнаружения, сек")
    plt.grid(True)
    plt.savefig("latency_vs_first_detection.png")
    plt.show()
 
    plt.figure(figsize=(8, 5))
    plt.plot(grouped["latency_max"], grouped["total_messages"], marker="o")
    plt.title("Влияние задержки на количество сообщений")
    plt.xlabel("Максимальная задержка доставки, сек")
    plt.ylabel("Количество сообщений")
    plt.grid(True)
    plt.savefig("latency_vs_messages.png")
    plt.show()
 
# =========================
# MAIN
# =========================
 
def main():
    print("Этап 1. Расчёт bandwidth")
    plot_bandwidth()
 
    print("\nЭтап 2-3. Сравнение Serf, Heartbeat и Ping")
    comparison_df = run_comparison(trials=20)
    plot_comparison(comparison_df)
 
    print("\nИндивидуальное задание. Влияние latency 0-500 мс")
    latency_df = run_latency_experiment(trials=15)
    plot_latency_experiment(latency_df)
 
    print("\nГотово. Графики и CSV-файлы сохранены в текущей папке.")
 
if __name__ == "__main__":
    main()