def main():
    words = input().split()
    groups = {}

    for word in words:
        key = ''.join(sorted(word.lower()))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)

    sorted_groups = []
    for group in groups.values():
        sorted_group = sorted(group)
        sorted_groups.append(sorted_group)

    sorted_groups.sort(key=lambda x: x[0])

    for group in sorted_groups:
        print(' '.join(group))


if __name__ == "__main__":
    main()